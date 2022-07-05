import json
import os
# import MySQLdb
from dotenv import load_dotenv

path = os.path.dirname(os.path.abspath(__file__))

load_dotenv(path + "/../.env")


class Config(object):
    """
    docstring
    """
    PROJECT = 'oracle-node'

    '''
        Celery
        Worker
        config
    '''
    
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_TASK_RESULT_EXPIRES = os.getenv('CELERY_TASK_RESULT_EXPIRES')
    CELERY_TASK_RESULT_EXPIRES = int(CELERY_TASK_RESULT_EXPIRES) if CELERY_TASK_RESULT_EXPIRES else 600
    CELERY_DEFAULT_QUEUE = 'oracle-calculating-queue'
    CELERY_ROUTES = {
        'worker.update_prices_to_smc': {'queue': 'oracle-calculating-queue'},
        'worker.update_public_prices_to_smc': {'queue': 'oracle-calculating-queue'},
    }
    CELERY_TRACK_STARTED = "True"
    CELERY_ENABLE_UTC = True
    CELERY_IMPORTS = ['src.workers']

    # Sentry
    # SENTRY_DSN = os.getenv('SENTRY_DSN')

    # Redis Cluster
    REDIS_CLUSTER = json.loads(os.getenv("REDIS_CLUSTER"))

    # Blockchain
    IS_GANACHE = int(os.getenv('IS_GANACHE')) if os.getenv('IS_GANACHE') else 0
    GANACHE_ACCOUNT = os.getenv('GANACHE_ACCOUNT') if IS_GANACHE else None
    
    RPC_URI = os.getenv('RPC_URI')
    # Deligate ORACLE CONTRACT ADDRESS
    iDelegateSeer = os.getenv('iDelegateSeer')

    # VECHAIN KEYSTORE PASSWORD
    KEYSTORE_PASSWORD = os.getenv('KEYSTORE_PASSWORD') or ''

    pass
