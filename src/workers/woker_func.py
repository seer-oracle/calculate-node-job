import sys
sys.path.append(".")
from src.task import worker
from src.utils import get_current_time
from src.helper import update_encoded_price_to_smc, set_public_prices_to_smc


@worker.task(name='worker.update_prices_to_smc', rate_limit='10/s')
def update_prices_to_smc(_encoded_price):
    try:
        update_encoded_price_to_smc(_encoded_price)
        return 'Update prices to SMC'
    except Exception as e:
        print(e)
        return None


@worker.task(name='worker.update_public_prices_to_smc', rate_limit='10/s')
def update_public_prices_to_smc(assets, prices):
    try:
        set_public_prices_to_smc(assets=assets, prices=prices)
        return 'Update public prices to SMC'
    except Exception as e:
        print(e)
        return None
