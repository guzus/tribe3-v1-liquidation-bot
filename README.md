# Tribe3 v1 Liquidation bot

## Overview

**Tribe3 v1 beta** (see [here](https://arbiscan.io/address/0x4309727ecf49205b441de39f68939b17222b98e3#code) for implementation) is vAMM based NFT perpetual exchange on Arbitrum. It has a liquidation mechanism that allows liquidators to profit by rectifying undercollateralized positions.

This bot is designed to capture liquidation opportunities and liquidate positions on Tribe3 v1.

## Running the bot

1. Deploy `LiquidationReader` contract on Arbitrum
2. Run `Arbitrum node` (see [here](https://docs.arbitrum.io/node-running/quickstart-running-a-node) for instructions)
3. Configure `.env` file
4. Run the `bot` on **Python 3.10+**

```
cd bot
pip install -r requirements.txt
python3 run.py
```

For optimal performance of this bot, it's crucial to minimize the latency of the eth_call function. It is recommended to run both the Arbitrum full node and the bot on the same machine.

## Important Note

Please be aware that since Tribe3 v1 beta is closed, the code provided here might require modifications to be applicable to other protocols.
