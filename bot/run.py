from type import Amm, Wallet
from pools import get_amms
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.middleware import validation
from abi import (
    ClearingHouseAbi,
    LiquidationReaderAbi,
)
from telegram import send_telegram_notification
from config import *
from traders import get_traders_by_arbiscan, get_traders_from_cache_file
from datetime import datetime
import asyncio
import sys

validation.METHODS_TO_VALIDATE = []
NULL_ADDRESS = "0x0000000000000000000000000000000000000000"


class Liquidator:
    def __init__(self, wallet: Wallet, amms: list[Amm], use_cache_for_traders=True):
        self.amms = amms
        self.wallet = wallet
        self.web3 = AsyncWeb3(AsyncHTTPProvider(NODE_URL))
        self.liquidation_reader_contract = self.web3.eth.contract(
            address=LIQUIDATION_READER_ADDRESS, abi=LiquidationReaderAbi
        )
        self.clearing_house_contract = self.web3.eth.contract(
            address=TRIBE3_CLEARING_HOUSE_ADDRESS, abi=ClearingHouseAbi
        )
        self.use_cache_for_traders = use_cache_for_traders
        self.network_io_cnt = 0
        self.network_io_sum = 0.0

        # use multiple nodes
        self.liquidation_reader_contracts = []
        for i in range(len(amms)):
            node_url = NODE_URLS[i % len(NODE_URLS)]
            print(f"amm{i} node url: {node_url}")
            web3 = AsyncWeb3(AsyncHTTPProvider(node_url))
            contract = web3.eth.contract(
                address=LIQUIDATION_READER_ADDRESS, abi=LiquidationReaderAbi
            )
            self.liquidation_reader_contracts.append(contract)

    async def start(self):
        if self.use_cache_for_traders:
            self.traders = get_traders_from_cache_file()
        else:
            current_block_number = await self.web3.eth.block_number
            self.traders = get_traders_by_arbiscan(current_block_number)
        print("traders length:", len(self.traders))

        # concurrent search
        k = 9
        tasks = []
        for i in range(0, len(self.amms), k):
            from_index = i
            to_index = min(i + k, len(self.amms))
            task = self.liquidate_by_amm_bulk(self.amms[from_index:to_index])
            tasks.append(task)
        print("tasks length:", len(tasks))
        for result in asyncio.as_completed(tasks):
            await result

    async def liquidate_by_amm_bulk(self, amms: list[Amm]):
        while True:
            target_amm, target_trader, ok = await self.get_liquidation_target_bulk(
                amms, self.traders
            )
            if ok:
                await self.post_order(target_amm, target_trader)
            if self.network_io_cnt % 10 == 0 and self.network_io_cnt > 0:
                print(
                    f"avg network io time: {int(self.network_io_sum) // self.network_io_cnt}ms"
                )
                self.wallet.update_nonce()

    async def get_liquidation_target_bulk(
        self, amm: list[Amm], traders: list[str]
    ) -> tuple[str, str, bool]:
        try:
            t = datetime.now()
            amm_addresses = [a.address for a in amm]
            liquidation_reader_contract = self.liquidation_reader_contract
            (
                target_amm,
                target_trader,
            ) = await liquidation_reader_contract.functions.getLiquidationTargetsInMultipleAmm(
                amm_addresses, traders
            ).call()
            latency = datetime.now() - t
            print(f"time taken: {int(latency.total_seconds() * 1000)}ms")
            self.network_io_cnt += 1
            self.network_io_sum += latency.total_seconds() * 1000
        except Exception as e:
            print("error:", e)
            return "", "", False

        if target_trader == NULL_ADDRESS:
            return "", "", False

        return target_amm, target_trader, True

    async def post_order(self, amm: str, trader: str):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")
        print("Posting order")

        try:
            liquidate_func = await self.clearing_house_contract.functions.liquidate(
                amm, trader
            ).build_transaction(
                {
                    "chainId": self.wallet.chain_id,
                    "from": self.wallet.public_key,
                    "nonce": self.wallet.nonce,
                    "gas": 1_500_000,
                    "gasPrice": self.web3.to_wei(
                        4, "gwei"  # hardcoded redundant gas price
                    ),
                }
            )

            signed_tx = self.web3.eth.account.sign_transaction(
                liquidate_func, private_key=self.wallet.private_key
            )

            send_tx = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

            tx_receipt = await self.web3.eth.wait_for_transaction_receipt(send_tx)
            print(tx_receipt)

            self.wallet.nonce += 1
            send_telegram_notification(
                f"{current_time}\nliquidating {trader} on {amm} : {tx_receipt}"
            )
        except Exception as e:
            print("error:", e)
            send_telegram_notification(
                f"{current_time}\nliquidating {trader} on {amm} : failed {e}"
            )

        return


if __name__ == "__main__":
    use_cache = False
    if len(sys.argv) > 1:
        use_cache = sys.argv[1] == "true"

    wallet = Wallet(EXECUTOR_PUBLIC_KEY, EXECUTOR_PRIVATE_KEY)
    amms: list[Amm] = get_amms()

    print("=============Tribe3 liquidator Just Woke Up=============")
    print("author : https://github.com/guzus")
    print("twitter : https://x.com/uncanny_guzus")
    print(f"executor: {wallet.public_key}\nnonce: {wallet.nonce}")
    print(f"use cache: {use_cache}")
    print("=============Tribe3 liquidator Just Woke Up=============")

    liquidator = Liquidator(wallet, amms, use_cache)
    asyncio.run(liquidator.start())
