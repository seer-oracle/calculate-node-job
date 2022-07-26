"""
    ----------------------------------------
    @notice: Helper funciton for oracle node
    * Author: Pham Anh Tai
    * Created date: May 05th, 2022
    ----------------------------------------
"""

import sys
sys.path.append(".")
from datetime import datetime as dt
from datetime import timezone
import json
import string
import struct
from subprocess import call
from src.extensions import redis_cluster
import numpy as np
from src.constants import Constants
from src.Price import BinaryPrices
from src.config import Config
from thor_requests.connect import Connect
from thor_requests.contract import Contract
from thor_requests.wallet import Wallet
import json
import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware



"""
    Function that allow gen key redis for price
"""


def gen_price_key(symbol, time_stamp, dex_name):
    return f"P_{symbol}_{time_stamp}_{dex_name}"


""" * Get time now in UTC by timestamp * """


def utc_timestamp_now():
    return dt.utcnow().replace(tzinfo=timezone.utc).timestamp()


"""
    Get single price from redis
    @params: _symbol
    @params: _dex_name
    @params: _time
    @return: value of price of symbol '_symbol' on Dex '_dex_name' at '_time' 
"""


def get_single_price_from_redis(_symbol="BTCBUSD", _dex_name="Binance", _time=0):
    _key = f"Oracle:price_{_symbol}_{_time}_{_dex_name}"
    _val = redis_cluster.get(_key)
    if _val:
        return float(_val)
    else:
        return 0



"""
    Write expirable value to redis
    @params: _key: string
    @return: 0 (Failed) or 1 (Success)
"""


def save_expirable_to_redis(key: string, value: string, time=Constants.TTL_DEFAULT):
    return redis_cluster.setex(name=key, value=value, time=time)


"""
    Write expirable value to redis
    @params: _key: string
    @return: 0 (Failed) or 1 (Success)
"""


def get_expirable_to_redis(name: string):
    return redis_cluster.get(name=name)


"""
    Write non-expirable value to redis
    @params: _key: string
    @return: 0 (Failed) or 1 (Success)
"""


def save_non_expirable_to_redis(key_name: string, field_name: string, value: string):
    return redis_cluster.hsetnx(key=key_name, name=field_name, value=value)


"""
    Function check redis key
    @params: key type HASH
    @return: value of the key
"""


def get_key_from_redis(redis_key: string, redis_field: string) -> string:
    return redis_cluster.hget(
            name=redis_key,
            key=redis_field
        )


"""
    Generate key for storing price after calculating
    @params:
        + symbol: Pair of symbol of price
        + timestamp: timestamp of price when storing
    @return: key formarted !
"""


def gen_storing_calculating_price_key(symbol: string, timestamp: int):
    return f"Oracle:calculated_price:{symbol}_{timestamp}"


"""
    Function: Get latest key available
    @return: latest timestamp have 
"""


def get_latest_key():

    _now = int(round(utc_timestamp_now(), 0))
    _check_times = 0

    while not redis_cluster.get(name=f"Oracle:price_BTCBUSD_{_now}_Binance"):
        _now -= 1
        _check_times += 1
        print(f"{_check_times} check at {_now} ")
        if _check_times > 10:
            _now = None
            break

    return _now



"""
    Function: call to price-smc and update prices
"""


def update_encoded_price_to_smc(_encoded_price: int):

    if not Config.IS_GANACHE:
        # Load keystore for login wallet
        key_dict = {}
        with open('src/keystore') as f:
            key_dict = json.load(f)

        # Establish connect to iDelegateSeer contracts
        connector = Connect(Config.RPC_URI)
        
        wallet = Wallet.fromKeyStore(ks=key_dict, password=Config.KEYSTORE_PASSWORD)
        
        # Contract iDelegateSeer
        iDelegateSeerAddress = Config.iDelegateSeer
        delegate_contract_instance = Contract.fromFile('src/iDelegateSeerABI.json')
        
        # Call update
        res = connector.transact(
            wallet,
            delegate_contract_instance,
            "updatePrices",
            [_encoded_price],
            iDelegateSeerAddress
        )
        print(f'*** Update prices {_encoded_price} to Oracle : {res}')

    else:

        # Establish to ganache server
        w3 = Web3(Web3.HTTPProvider(Config.RPC_URI))
        # set pre-funded account as sender
        w3.eth.default_account = Config.GANACHE_ACCOUNT

        with open('src/iDelegateSeerABI.json') as f:
            abi = json.loads(f.read())['abi']
        delegation_contract = w3.eth.contract(Config.iDelegateSeer, abi=abi)

        # Inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Call update
        tx_hash = delegation_contract.functions.updatePrices(_encoded_price).transact()
        print(f"*** UPDATE PRICE TO GANACHE {_encoded_price} by tx {tx_hash}")

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"*** Receipt for {tx_hash} : {tx_receipt}")
    
    pass


"""
    Function that update public prices to SMC
"""


def set_public_prices_to_smc(assets, prices):
    print('PUBLIC PRICES UPDATING : ', assets, prices)
    if not Config.IS_GANACHE:
        # Load keystore for login wallet
        key_dict = {}
        with open('src/keystore') as f:
            key_dict = json.load(f)

        # Establish connect to iDelegateSeer contracts
        connector = Connect(Config.RPC_URI)
        
        wallet = Wallet.fromKeyStore(ks=key_dict, password=Config.KEYSTORE_PASSWORD)
        
        # Contract SeerForEachPair
        _contract_instance = Contract.fromFile('src/iSeerOracleForEachPair.json')

        for i in range(len(assets)):
            if prices[i] == 0:
                continue
            _price = prices[i]
            # Call update
            res = connector.transact(
                wallet,
                _contract_instance,
                "updateAnswer",
                [_price],
                assets[i]
            )
            print(f"*** Update public = {res}")

        print(f'*** Update public price {assets, prices} to Oracle ')

    else:

        # Establish to ganache server
        w3 = Web3(Web3.HTTPProvider(Config.RPC_URI))
        # set pre-funded account as sender
        w3.eth.default_account = Config.GANACHE_ACCOUNT

        with open('src/iSeerOracleForEachPair.json') as f:
            abi = json.loads(f.read())['abi']

        # Inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        for i in range(len(assets)):
            _contract = w3.eth.contract(assets[i], abi=abi)
            # Call update
            tx_hash = _contract.functions.updateAnswer(prices[i]).transact()
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"*** Receipt for {tx_hash} : {tx_receipt}")

        print(f"*** UPDATE PRICE TO GANACHE {assets, prices} by tx {tx_hash}")
    
    pass


"""
    Function check if changing rate of price is big enough or not
"""


def is_price_diff_enough(prev_price, current_price, compare_list, index):
    if prev_price == 0:
        return True
    _diff_factor = compare_list[index]
    return abs(current_price - prev_price) / prev_price > _diff_factor


def average(_list: list):
    if len(_list) == 0:
        return 0
    return sum(_list) / len(_list)
