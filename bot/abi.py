PositionChangedEventAbi = [
    {
        "type": "event",
        "name": "PositionChanged",
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "trader",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "amm",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "margin",
                "type": "int256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "positionNotional",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "exchangedPositionSize",
                "type": "int256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "fee",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "positionSizeAfter",
                "type": "int256",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "realizedPnl",
                "type": "int256",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "unrealizedPnlAfter",
                "type": "int256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "badDebt",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "liquidationPenalty",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "spotPrice",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "fundingPayment",
                "type": "int256",
            },
        ],
    }
]

MaintenanceMarginRatioMethodAbi = [
    {
        "type": "function",
        "name": "maintenanceMarginRatio",
        "inputs": [],
        "outputs": [{"type": "uint256"}],
    }
]

GetMarginRatioMethodAbi = [
    {
        "type": "function",
        "name": "getMarginRatio",
        "inputs": [
            {"name": "_amm", "type": "address"},
            {"name": "_trader", "type": "address"},
        ],
        "outputs": [{"type": "int256"}],
    }
]

LiquidateMethodAbi = [
    {
        "inputs": [
            {"internalType": "contract IAmm", "name": "_amm", "type": "address"},
            {"internalType": "address", "name": "_trader", "type": "address"},
        ],
        "name": "liquidate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

GetPositionMethodAbi = [
    {
        "inputs": [
            {"internalType": "contract IAmm", "name": "_amm", "type": "address"},
            {"internalType": "address", "name": "_trader", "type": "address"},
        ],
        "name": "getPosition",
        "outputs": [
            {
                "components": [
                    {"internalType": "int256", "name": "size", "type": "int256"},
                    {"internalType": "int256", "name": "margin", "type": "int256"},
                    {
                        "internalType": "uint256",
                        "name": "openNotional",
                        "type": "uint256",
                    },
                    {
                        "internalType": "int256",
                        "name": "lastUpdatedCumulativePremiumFraction",
                        "type": "int256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct IClearingHouse.Position",
                "name": "",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


ClearingHouseAbi = [
    PositionChangedEventAbi[0],
    GetMarginRatioMethodAbi[0],
    LiquidateMethodAbi[0],
    GetPositionMethodAbi[0],
]

LiquidationReaderAbi = [
    {
        "inputs": [
            {"internalType": "contract IAmm", "name": "amm", "type": "address"},
            {"internalType": "address[]", "name": "traders", "type": "address[]"},
        ],
        "name": "getLiquidationTargets",
        "outputs": [{"internalType": "address", "name": "trader", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "contract IAmm[]", "name": "amms", "type": "address[]"},
            {"internalType": "address[]", "name": "traders", "type": "address[]"},
        ],
        "name": "getLiquidationTargetsInMultipleAmm",
        "outputs": [
            {"internalType": "address", "name": "amm", "type": "address"},
            {"internalType": "address", "name": "trader", "type": "address"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]
