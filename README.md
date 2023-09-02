# Tribe3 v1 Liquidation bot

## Overview

**Tribe3 v1 beta** (see [here](https://arbiscan.io/address/0x4309727ecf49205b441de39f68939b17222b98e3#code) for implementation) is vAMM based NFT perpetual exchange on Arbitrum. It has a liquidation mechanism that allows liquidators to profit by rectifying undercollateralized positions.

This bot is designed to capture liquidation opportunities and liquidate positions on Tribe3 v1.

## Running the bot

1. Deploy `LiquidationReader` contract on Arbitrum
2. Run `Arbitrum node` (see [here](https://docs.arbitrum.io/node-running/quickstart-running-a-node) for instructions)
3. Configure `.env` file
4. Run the `bot` on **Python 3.10+**

```shell
cd bot
pip install -r requirements.txt
python3 run.py
```

For optimal performance of this bot, it's crucial to minimize the latency of the eth_call function. It is recommended to run both the Arbitrum full node and the bot on the same machine.

## Algo

```python
"""
1. get a list of EOAs that have sent ETH to Tribe3 ClearingHouse contract by using arbiscan API

2. loop infinitely(in my case it took 300 ms per cycle):
    
    eth_call to smart contract(LiquidationReader) to get a trader address and pool address of undercollateralized position
    
    if there's any:
        
        send a transaction to liquidate the position

        send telegram notification (success / failure)
"""
```

## More Optimizations that could have been done

- Compare gas fee and a profit of liquidating a position, and only liquidate if the profit is greater than the gas fee

- Save gas fee by creating ordering contract. e.g. only pass the address of trader to the ordering contract, and let the ordering contract call the liquidation contract with every(eight) pool addresses. This way, we can save gas fee by optimizing calldata.

- `eth_call` faster so that we can run eth_call faster than block creation speed(250ms / block).

## Important Note

Please be aware that since Tribe3 v1 beta is closed, the code provided here might require modifications to be applicable to other protocols.
