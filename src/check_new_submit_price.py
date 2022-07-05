from ast import Constant
from helper import get_key_from_redis
import time
from constants import Constants

def main():
    """
        No running affective now !!!
    """
    while True:
        for index_of_symbol in Constants.LIST_SYMBOL:
            _key_available_new_price = f"Oracle_available_new_price_{Constants.LIST_SYMBOL[index_of_symbol]}"
            get_key_from_redis()
        time.sleep(1)
        pass

if __name__ == '__main__':
    main()