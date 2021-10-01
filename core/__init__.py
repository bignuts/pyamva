# def __calc_rates(self, symbol: str, timeframe: ITimeframe, target: Union[int, datetime], decimal: int, offset: int) -> pd.DataFrame:
#     if isinstance(target, int):
#         r = self.__g.get_rates(symbol, timeframe, 0, target)
#     if isinstance(target, datetime):
#         r = self.__g.get_rates(symbol, timeframe, DTU.utc_now(), target)
#     r = self.__a.adapt(r, decimal, offset)
#     r = self.__c.convert(r)
#     return r

import datetime
from typing import Optional

from pandas import DataFrame, Series
from connectors import MetaTrader
from MetaTrader5 import TIMEFRAME_M30
from pandas import to_datetime


def calc_rates():
    # TODO se si vuole l'index come ragiona metatrader bisogna dare rates[::-1]
    mt = MetaTrader()
    rates = mt.get_rates('EURUSD', TIMEFRAME_M30, 0, 500)
    # aggiungere offset prima di trasformare in df
    df = DataFrame(rates)
    df = df.set_index('time')
    df.to_csv("original.csv")
    days = df.resample('D').max()
    days = days.dropna(how='all')
    # days = df.resample('D', on='time').max() nel caso 'time' non fosse indice
    days['day_name'] = days.index.day_name()
    days['tz'] = days.index.tz
    days.to_csv('days.csv')
    print(days)

    # aggiunge offset
    # converte time in formato datetime e aggiunge offste per togliere i
    # sabati e domeniche
    # df['time'] = to_datetime(df['time'], unit='s')
    # df['addtime'] = df['time'] + datetime.timedelta(hours=2)
    # setta nuovo indice
    # df = df.astype({'time': 'datetime64[ns]'})
    # df = df.set_index('time')
    # print(df.dtypes)
    # days = df.resample('D').max()
    # print(days)


def days_in_df(src_df: DataFrame, on: Optional[str]) -> Series:
    # resample e restituisce i giorni nel df e lo inverte
    dst_df = src_df.resample('D', on=on).max().iloc[::-1]
    # aggiunge colonna con il nome della settimana
    dst_df['day_of_week'] = dst_df['date'].dt.day_name()
    dst_df.to_csv('series.csv')
    # rimuove le righe cha hanno valori vuote
    dst_df = dst_df.dropna(how='all')
    # converte DateTimeIndex in series
    # dst_df = dst_df.index.to_series(
    #     index=[i for i in range(len(dst_df))], keep_tz=True)
    return dst_df
