import datetime
from typing import Optional

from pandas import DataFrame, Series
from connectors import MetaTrader
from MetaTrader5 import TIMEFRAME_M30
from pandas import to_datetime

# da guardare
# adapter trasforma le rates in tpo <== qua e poi
# marketscreen
# profile_ <== qua create profile from rates
# rates --- fatto
# reference
# report


def calc_rates():
    # TODO se si vuole l'index come ragiona metatrader bisogna dare rates[::-1]
    mt = MetaTrader()
    rates = mt.get_rates('EURUSD', TIMEFRAME_M30, 0, 2000)
    # aggiungere offset prima di trasformare in df
    df = DataFrame(rates)
    df = df.set_index('time')
    df.to_csv('oro.csv')
    # Errore se ci sono dei sabbati / domeniche
    if check_saturday_sunday(df):
        raise Exception('Ci sono dei sabati e delle domeniche')


def days_in_df(df: DataFrame) -> DataFrame:
    days = df.resample('D').max()
    days = days.dropna(how='all')
    days['day_name'] = days.index.day_name()
    days['tz'] = days.index.tz
    return days[['day_name', 'tz']]


def check_saturday_sunday(df: DataFrame) -> bool:
    days = days_in_df(df)
    check_res = ((days['day_name'] == 'Saturday') |
                 (days['day_name'] == 'Sunday')).any()
    return check_res
