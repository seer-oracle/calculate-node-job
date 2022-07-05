# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import sys
sys.path.append(".")
from src.worker_lib import create_worker
from src.config import Config


worker = create_worker(Config)
