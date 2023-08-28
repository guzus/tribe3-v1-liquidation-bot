from config import *
import requests
from web3 import Web3


def get_traders_by_arbiscan(current_block_number: int) -> list[str]:
    print("=============Fetching tribe3 interactors using arbiscan.io api=============")

    traders = set()
    base_url = "https://api.arbiscan.io/api"

    i = TRIBE3_CONTRACT_CREATION_BLOCK
    while i <= current_block_number:
        interval = 5000000  # approx 2 weeks
        query = f"?module=account&action=tokentx&address={TRIBE3_CLEARING_HOUSE_ADDRESS}&startblock={i}&endblock={i+interval-1}&sort=asc&apikey={ARBISCAN_API_KEY}"
        resp = requests.get(base_url + query)
        if resp.status_code == 200:
            res = resp.json()
            result = res["result"]
            for r in result:
                from_addr = r["from"]
                if from_addr != TRIBE3_CLEARING_HOUSE_ADDRESS:
                    from_addr = Web3.to_checksum_address(from_addr)
                    traders.add(from_addr)
        i += interval

    # cache to text file
    f = open("traders.txt", "w")
    f.write(",".join(traders))
    f.close()

    traders = list(traders)

    return traders


def get_traders_from_cache_file() -> list[str]:
    f = open("traders.txt", "r")
    traders = f.read().split(",")
    f.close()
    return traders
