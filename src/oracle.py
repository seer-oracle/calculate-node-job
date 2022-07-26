import sys
import time
from helper import get_latest_key, utc_timestamp_now, \
    get_single_price_from_redis, get_key_from_redis, save_non_expirable_to_redis, gen_storing_calculating_price_key, \
    is_price_diff_enough, average, save_expirable_to_redis, get_expirable_to_redis
from Price import *
from constants import Constants
import statistics
from src.workers import update_prices_to_smc, update_public_prices_to_smc
sys.path.append('.')


def main():
    
    _now = utc_timestamp_now()
    print('*** Time start jobs : ', _now)

    # Hard-code initial value for test only data of BTCBUSD in Binance
    # _now = 1651646625
    # _symbol = 'BTCUSD'  # Hard-code symbol

    # Start calculating by EMA(Exponential Moving Average)
    EMA = [0] * len(Constants.LIST_SYMBOL)
    _time = [0] * len(Constants.LIST_SYMBOL)

    _prev_price_list = [0] * len(Constants.PRICE_DIFF)
    _price_list = [0] * len(Constants.PRICE_DIFF)

    _prev_public_price_list = [0] * len(Constants.LIST_SUB_PUBLIC_SYMBOLS)

    #  Loop the jobs
    while True:

        log_time = utc_timestamp_now()
        print('Time Loop jobs : ', log_time)

        _now = get_latest_key()
        print('latest key = ', _now)
        if not _now:
            time.sleep(5)
            continue

        # only for easy-readable
        print('_' * 50)
        print()

        # Check function is used in redis
        choosing_function = get_key_from_redis(
                redis_key=Constants.CHOOSING_FUNCTION_REDIS_KEY,
                redis_field=Constants.CHOOSING_FUNCTION_REDIS_FIELD
            )
        if not choosing_function:
            save_non_expirable_to_redis(
                key_name=Constants.CHOOSING_FUNCTION_REDIS_KEY,
                field_name=Constants.CHOOSING_FUNCTION_REDIS_FIELD,
                value="median"    
            )
            choosing_function = "median"
        print('Oracle choosing Function ', choosing_function)

        ###
        #   Crawl data from redis and take EMA algorithm to calculate next EMA value for each pair
        ###
        for index_of_symbol in range(len(Constants.LIST_SYMBOL)):
            print('Current symbol = ', Constants.LIST_SYMBOL[index_of_symbol])

            if Constants.LIST_SYMBOL[index_of_symbol] == 'VEUSDBUSD':
                EMA[index_of_symbol] = 1
                continue

            # Get Price From list Dex
            _prices = []
            for _dex_name in Constants.LIST_DEX:
                _price = get_single_price_from_redis(
                    _symbol=Constants.LIST_SYMBOL[index_of_symbol],
                    _dex_name=_dex_name,
                    _time=_now
                )
                if _price != 0:
                    _prices.append(_price)
            print('prices = ', _prices)

            # Choose Price for calculating
            _prices = [item for item in _prices if item > 0]

            if len(_prices) == 0:
                continue

            if len(_prices) == 1:
                choosing_price = _prices[0]
            else:
                choosing_price = getattr(statistics, choosing_function)(_prices)
            
            print('Choosing Price = ', choosing_price)

            # Increase time of sliding window interval calculation
            _time[index_of_symbol] += 1
            
            # Check if initial calculation then set EMA = the first price
            # If not, then calculate with Exponential Moving Average

            if EMA[index_of_symbol] == 0:
                EMA[index_of_symbol] += choosing_price
            else:
                k_factor = Constants.SMOOTHING_FACTOR / (1 + _time[index_of_symbol])
                EMA[index_of_symbol] = EMA[index_of_symbol] * (1 - k_factor) + choosing_price * k_factor
            
            # Log EMA result for debug
            print(f"At {utc_timestamp_now()}  {_time[index_of_symbol]}_{_now} = {EMA[index_of_symbol]}")
            
            # Save to redis the final price of each calculation point of time
            key_redis = gen_storing_calculating_price_key(Constants.LIST_SYMBOL[index_of_symbol], _now)

            print('Save to redis with key : ', key_redis)
            value_redis = EMA[index_of_symbol]
            result = save_expirable_to_redis(
                key=key_redis,
                value=value_redis
            )
            print('**result = ', result)

            # Save latest update timestamp of each pair
            save_expirable_to_redis(key=f"{Constants.LIST_SYMBOL[index_of_symbol]}_last_timestamp", value=_now)

            # Check if the freshness of data
            # reset calculation start point when data reach limit of freshness
            if _time[index_of_symbol] >= Constants.FRESHNESS_PERIOD / Constants.SLIDING_WINDOW_INTERVAL:
                EMA[index_of_symbol] = 0
                _time[index_of_symbol] = 0

            # only for easy-readable
            print('     ', '_' * 40)
            print() 

        ###
        #       Update prices in one round to Oracle SMC
        ###
        print('EMA = ', EMA, len(EMA))

            ##     Update prices by bitwise operations for Defi Protocol (Pair/USD)

        raw_prices = []
        # check diff rate of price
        for i in range(len(Constants.PRICE_INDEX)):
            if len(raw_prices) < Constants.PRICE_INDEX[i] + 1:
                raw_prices.insert(Constants.PRICE_INDEX[i], [])
            if EMA[i] != 0:
                raw_prices[Constants.PRICE_INDEX[i]].append(EMA[i])
        print('raw : ', raw_prices)
        # Hardcode price of VEBANK
        vebank_hardcode = Constants.HARD_CODE_PRICE_VB

        # listing prices in raw
        print('raw 1 : ', raw_prices)
        raw_prices = [average(raw_prices[0]), average(raw_prices[1]), vebank_hardcode, average(raw_prices[2])]
        print('raw 2 : ', raw_prices)

        # Check price diff for defi prices
        _price_list = raw_prices
        _submit_list = []
        for i in range(len(_price_list)):
            if is_price_diff_enough(_prev_price_list[i], _price_list[i], Constants.PRICE_DIFF, i):
                _submit_list.append(_price_list[i])
            else:
                _submit_list.append(0)

        print('prev list = ', _prev_price_list)
        print('price_list = ', _price_list)
        print('_submit_list : ', _submit_list)
        # Beautify number
        for i in range(len(_submit_list)):
            _submit_list[i] = int(_submit_list[i] * (10 ** Constants.PRICE_DECIMALS[i]))
        print('_submit_list gather = ', _submit_list)

        if not all(_p == 0 for _p in _submit_list):
            # price bitwise list
            _price_bit = Constants.PRICE_BIT

            # Encode prices
            print('before encode !')
            _encoded_price = BinaryPrices.encode(_price_list=_submit_list, _price_bit=_price_bit)
            print(f"after encode : {_encoded_price}")
            # Do task
            update_prices_to_smc.delay(_encoded_price)
            for _index in range(len(_submit_list)):
                if _submit_list[_index] != 0:
                    _prev_price_list[_index] = _submit_list[_index]




            ##      Set price for public pair
        
        _public_prices = [*EMA, Constants.HARD_CODE_PRICE_VB, Constants.HARD_CODE_PRICE_VB]
        _choosing_public_prices = []
        for idx, _item in enumerate(_public_prices):
            if Constants.LIST_SYMBOL_INCLUDE_VB[idx] in Constants.LIST_SUB_PUBLIC_SYMBOLS:
                _choosing_public_prices.append(_item)
        _choosing_public_prices = [int(_item * 10 ** 18) for _item in _choosing_public_prices]
        print("Choosing public prices = ", _choosing_public_prices)
        # Check gap
        _public_submit_list = []
        for i in range(len(_choosing_public_prices)):
            if is_price_diff_enough(
                    _prev_public_price_list[i],
                    _choosing_public_prices[i],
                    Constants.PUBLIC_PRICE_DIFF,
                    i
                    ):
                _public_submit_list.append(_choosing_public_prices[i])
            else:
                _public_submit_list.append(0)

        if not all(_p == 0 for _p in _choosing_public_prices):
            # update_public_prices_to_smc.delay(
            #     assets=Constants.LIST_PUBLIC_PAIR_ADDRESS,
            #     prices=_public_submit_list
            # )
            for _index in range(len(_public_submit_list)):
                if _public_submit_list[_index] != 0:
                    _prev_public_price_list[_index] = _public_submit_list[_index]

        # Sleep to wait for next calculation
        time.sleep(5)

        # Increase point of time to check price
        # _now += Constants.SLIDING_WINDOW_INTERVAL
    
    # End of Loop for jobs
                

if __name__ == "__main__":
    main()

