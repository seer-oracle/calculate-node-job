
from typing import List


class BinaryPrices(object):
    @staticmethod
    def encode(_price_list: list, _price_bit: list):
        if len(_price_bit) != len(_price_list):
            return None
        
        _total_bit = 0
        _encoded = 0

        for i in range(len(_price_list)):
            _encoded |= _price_list[i] << _total_bit
            _total_bit += _price_bit[i]

        return _encoded

    @staticmethod
    def decode(price_bit: list, encoded_value):
        _total_bit = 0
        _decoded_vals = []
        for i in range(len(price_bit)):
            _decoded_val = (encoded_value >> _total_bit) & ((1 << price_bit[i]) - 1)
            print(f"{i}: {_decoded_val}")
            _decoded_vals.append(_decoded_val)
            _total_bit += price_bit[i]
        
        return _decoded_vals
