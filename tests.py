from util import rates_to_py_file
from connectors import MetaTrader
from datetime import datetime, timedelta
from MetaTrader5 import TIMEFRAME_H1, TIMEFRAME_M10, TIMEFRAME_M15, TIMEFRAME_M30, TIMEFRAME_D1

mt = MetaTrader()
rates = mt.get_rates(
    'EURUSD', TIMEFRAME_M30, datetime(
        2021, 9, 30, 0, 0, 0), datetime(
        2021, 9, 1, 0, 0, 0))

rates_to_py_file(rates, 'aaa.py')
