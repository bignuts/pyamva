from MetaTrader5 import TIMEFRAME_M30
from core import rates_to_tpo
from MetaTrader5 import TIMEFRAME_M30
from connectors import MetaTrader

mt = MetaTrader()
rates = mt.get_rates('EURUSD', TIMEFRAME_M30, 0, 2000)
rates_to_tpo(rates, 5, 5)
