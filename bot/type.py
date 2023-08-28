from dataclasses import dataclass
from typing import Optional
from web3 import Web3
from config import NODE_URL


@dataclass
class Amm:
    index: int
    address: str
    maintenance_margin_ratio: int
    symbol: Optional[str] = None

    def __post_init__(self):
        self.address = Web3.to_checksum_address(self.address)


class Wallet:
    def __init__(self, public_key: str, private_key: str):
        web3 = Web3(Web3.HTTPProvider(NODE_URL))
        self.public_key = Web3.to_checksum_address(public_key)
        self.private_key = private_key
        self.chain_id = web3.eth.chain_id
        self.update_nonce()

    def update_nonce(self):
        web3 = Web3(Web3.HTTPProvider(NODE_URL))
        nonce = web3.eth.get_transaction_count(self.public_key)
        self.nonce = nonce
        print(f"{self.public_key}: nonce updated to {nonce}")
