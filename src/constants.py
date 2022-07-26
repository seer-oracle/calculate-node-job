class Constants(object):
    SMOOTHING_FACTOR = 2
    FRESHNESS_PERIOD = 3600
    SLIDING_WINDOW_INTERVAL = 5
    TTL_DEFAULT = 86400

    LIST_DEX = [
        'Binance',
        'CoinBase',
        'Kraken',
        'Gemini',
        'Poliniex',
        'Kraken_CW',
        'Vexchange',
        'KuCoin',
        'OceanEx',
        'Houbi',
        'BitMart'
    ]

    LIST_SYMBOL = [
        'VTHOUSDT',     # 1
        'VTHOBUSD',
        'VTHOUSD',
        'VETUSDT',      # 2
        'VETBUSD',
        'VETUSD',
        'VEUSDUSDT',    # 3
        'VEUSDBUSD',
        'VEUSDUSD', 
        'BTCUSDT',      # 4
        'BTCBUSD',
        'BTCUSD',
        'ETHUSDT',      #5
        'ETHBUSD',
        'ETHUSD',
        # 'USDT',
        # 'BUSDUSDT',
        # 'VEXUSDT',
        # 'WVETUSDT',
        # 'VEBUSD',
        # 'BUSD',
        # 'USD',
        # 'BUSDUSD',
        # 'VEXUSD', 
        # 'WVETUSD'
    ]

    LIST_SYMBOL_INCLUDE_VB = [
        'VTHOUSDT',     # 1
        'VTHOBUSD',
        'VTHOUSD',
        'VETUSDT',      # 2
        'VETBUSD',
        'VETUSD',
        'VEUSDUSDT',    # 3
        'VEUSDBUSD',
        'VEUSDUSD', 
        'BTCUSDT',      # 4
        'BTCBUSD',
        'BTCUSD',
        'ETHUSDT',      #5
        'ETHBUSD',
        'ETHUSD',
        'VBUSDT',
        'VBBUSD'
    ]

    LIST_SUB_PUBLIC_SYMBOLS = [
        'VTHOUSDT',     # 1
        'VTHOBUSD',
        'VETUSDT',      # 2
        'VETBUSD',
        'VEUSDUSDT',    # 4
        'VEUSDBUSD',
        'BTCUSDT',      # 5
        'BTCBUSD',
        'BTCUSD',
        'ETHUSDT',      # 6
        'ETHBUSD',
        'ETHUSD',
        'VBUSDT',       # 7
        'VBBUSD'
    ]

    LIST_PUBLIC_PAIR_ADDRESS = [
        '0xb448016Ee01Db3b219963997FD5E08026A07e60c',   # VETHO/USDT
        '0xA6Ea4B667E2e44896a4cC3F49A77Ba8c3fEcC740',   # VETHO/BUSD
        # '0x5E7A52743575FE6F8cD8937C0415640338eBdd29',   # VETHO/USD
        '0xa6cF09E6cC15cCBC0b7Fb8e0287710fDdfDBB7f6',   # VET/USDT
        '0x59Bb2E6E9C8bDb2F1d701d29827c1C7b44F0A8Aa',   # VET/BUSD
        # '0x3212feD5581DEFbb2d7Ea21d7F22f657cD3da97E',   # VET/USD
        '0xFDcC10429fA96bfD0E5FF7b76c7Da6156933BBB3',   # VEUSD/USDT
        '0x4762F8647a763fB7599AdDf792E80897855b3294',   # VEUSD/BUSD
        # '0xA2B0d7b38dc13a58A7B4c0E8E2400d650dad46EC', # VEUSD/USD
        '0x51160f0383913De0F31A848f0263F9b00AD09563',   # BTC/USDT
        '0x3Dd64A69a5ED7E6058ed533a8B8Bdf0527652dA8',   # BTC/BUSD
        '0x18A2fEAae2fA06B3452fd094Ba802C93FF0dA972',   # BTC/USD
        '0x6A90EbA99ec7006eFD9AB5cA645cE291BB32924c',   # ETH/USDT
        '0x5e6790995dd9F5A0f8D85EaCB101ac294D7323ae',   # ETH/BUSD
        '0xed8e829cfEB0Cdd315C26c7df10e81B12a3abA95',   # ETH/USD
        '0xa366913D8E8FdcE13c58d5F20DF8C27f77BFF8AE',   # VB/USDT
        '0xB92b92da7122937436cAa2bbd9B22c837cB1023C',   # VB/BUSD
        # '0xDf925feC9932A1De0d2b4404cCfac09166624F94',   # VB/USD
    ]

    PRICE_BIT = [
        57,
        57,
        57,
        37
    ]

    PRICE_DECIMALS = [
        12,
        12,
        12,
        6
    ]

    PRICE_INDEX = [
        0,
        0,
        0,
        1,
        1,
        1,
        2,
        2
    ]
    PRICE_DIFF = [
        0.01,
        0.01,
        0.01,
        0.01
    ]

    PUBLIC_PRICE_DIFF = [
        0.01,
        0.01,
        0.01,
        0.01,
        0.01,
        0.01,
        0.02,
        0.02,
        0.02,
        0.02,
        0.02,
        0.02,
        0.01,
        0.01
    ]

    CHOOSING_FUNCTION_REDIS_KEY = 'Oracle:choosing_function'
    CHOOSING_FUNCTION_REDIS_FIELD = 'function'
    HARD_CODE_PRICE_VB = 10.12315
