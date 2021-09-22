import pandas as pd
from math import ceil, floor
from util import DataFrameUtil as DFU
from datetime import timedelta, datetime
from typing import List, Tuple


class CreateProfile:
    """Classe per la trasformazione da Rates a Profile"""

    # https://stackoverflow.com/questions/53927460/select-rows-in-pandas-multiindex-dataframe
    def from_rates(self, rates: pd.DataFrame, tpo_size: int) -> pd.DataFrame:
        """Crea Profile dalle Rates"""

        # round low
        rates.loc[:, 's_low'] = rates['low'].apply(
            self.__low_round, tpo_size=tpo_size)
        # round high
        rates.loc[:, 's_high'] = rates['high'].apply(
            self.__high_round, tpo_size=tpo_size)

        # find high
        high = rates['s_high'].max()
        # find low
        low = rates['s_low'].min()
        # create range
        rng = self.__create_range(low, high, tpo_size)

        df = pd.DataFrame(None,
                          columns=rng,
                          index=rates['date'],
                          dtype='int8')

        self.__populate_df(rates, df)

        return df

    def __create_range(self, low: int, high: int, step: int) -> List[int]:
        return [x for x in range(low, high, step)]

    def __populate_df(self, rates: pd.DataFrame, df: pd.DataFrame) -> None:
        """Prende il profile e lo popola di 1"""
        # TODO si può ottimizzare probabilmente
        for row in rates.itertuples():
            df.loc[row.date, row.s_low:row.s_high] = 1

    def __high_round(self, high: int, tpo_size: int) -> int:
        return (ceil(high / tpo_size) * tpo_size)

    def __low_round(self, low: int, tpo_size: int) -> int:
        return floor(low / tpo_size) * tpo_size

    def from_main_profile(self, main_profile: pd.DataFrame, frm: int, count: int) -> pd.DataFrame:
        """Crea un Sub_Profile dal Main_Profile"""
        return DFU.slice_by_days(main_profile, None, frm, count).dropna(how='all', axis=1)
