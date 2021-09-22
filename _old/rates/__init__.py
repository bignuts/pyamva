import pandas as pd
from getter import IGetter
from adapter import IAdapter
from converter import IConverter
from datetime import datetime, timedelta
from util import DateTimeUtil as DTU
from util import DataFrameUtil as DFU
from typing import Dict, Union
import pytz
from timeframes import ITimeframe, Timeframe
from database import Param


class Rates:
    """Classe per l'acquisizione e la rasformazione delle rates"""

    def __init__(self, g: IGetter, a: IAdapter, c: IConverter):
        self.__g = g
        self.__a = a
        self.__c = c

    def get_rates(self, db: Param) -> pd.DataFrame:

        timeframe = Timeframe(db.timeframe)
        days = db.days
        symbol = db.symbol
        decimal = db.decimal
        offset = db.offset

        # timeframe in un giorno * i giorni comprese sabato e domenica
        # TODO in realtà stiamo chiedendo più rates del dovuto
        times = round((1440/timeframe.value)*(days*(7/5)))

        # calcola le rates e ritorna un df
        r = self.__calc_rates(symbol, timeframe, times, decimal, offset)

        # controlla che ci siano effettivamente 50 giorni
        while not self.__check_days(r, days):
            times += round((1440/timeframe.value)*10)
            # TODO invece che ricalcolare si potrebbe appendere una selezione più limitata di valori
            r = self.__calc_rates(symbol, timeframe, times, decimal, offset)

        # slice per ritornare meno giorni
        r = DFU.slice_by_days(r, 'date', 0, days)

        return r

    def __calc_rates(self, symbol: str, timeframe: ITimeframe, target: Union[int, datetime], decimal: int, offset: int) -> pd.DataFrame:
        if isinstance(target, int):
            r = self.__g.get_rates(symbol, timeframe, 0, target)
        if isinstance(target, datetime):
            r = self.__g.get_rates(symbol, timeframe, DTU.utc_now(), target)
        r = self.__a.adapt(r, decimal, offset)
        r = self.__c.convert(r)
        return r

    def __check_days(self, rates: pd.DataFrame, days: int) -> bool:
        df = DFU.days_in_df(rates, 'date')
        return len(df) > days
