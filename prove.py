from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from MetaTrader5 import TIMEFRAME_M30

#https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
  
# Getting the current date
# and time
dt = datetime(2021, 9, 20, 15, tzinfo=ZoneInfo('Europe/Rome'))
print(dt)
print(dt.tzname())
  
utc_time = dt.astimezone(timezone.utc)
print(utc_time)
print(utc_time.tzname())

from connectors import MetaTrader

mt = MetaTrader()
to = datetime(2021, 7, 20, 15, 25, 36, tzinfo=timezone.utc)
frm = to - timedelta(days=15)
rates_df1 = mt.get_rates("EURUSD", TIMEFRAME_M30, frm, to)
rates_df1.to_csv('prove.csv')