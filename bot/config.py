import os
from dotenv import load_dotenv


load_dotenv(verbose=True)

TRIBE3_CLEARING_HOUSE_ADDRESS = "0x01b6407ADf740d135ddF1eBDD1529407845773F3"
TRIBE3_CONTRACT_CREATION_BLOCK = 79753986

EXECUTOR_PUBLIC_KEY = os.getenv("EXECUTOR_PUBLIC_KEY")
EXECUTOR_PRIVATE_KEY = os.getenv("EXECUTOR_PRIVATE_KEY")

ARBISCAN_API_KEY = os.getenv("ARBISCAN_API_KEY")
LIQUIDATION_READER_ADDRESS = os.getenv("LIQUIDATION_READER_ADDRESS")

# change this to your node url
NODE_URL = "http://127.0.0.1:8547"
NODE_URLS = [
    "http://127.0.0.1:8547",
]

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")