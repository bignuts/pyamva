from typing import Callable, List
from numpy import around, floor, ceil
from pandas import DataFrame, Series
from connectors.models import Rates


def _check_saturday_sunday(df: DataFrame) -> bool:
    days = _days_in_df(df)
    days.to_excel('./xlsx/days.xlsx')
    check_res = ((days['day_name'] == 'Saturday') |
                 (days['day_name'] == 'Sunday')).any()
    return check_res


def _days_in_df(df: DataFrame) -> DataFrame:
    '''
    Il df: Dataframe deve avere come indice un DatetimeIndex
    '''
    days = df.resample('D').max()
    days = days.dropna(how='all')
    days['day_name'] = days.index.day_name()
    days['tz'] = days.index.tz
    return days[['day_name', 'tz']]


class Tpo:

    def from_rates(self, rates: List[Rates],
                   decimal: int, tpo_size: int) -> DataFrame:
        '''
        Da rates: List[Rates] restituisce un DataFrame come segue

        | index         | tpo1    | tpo2    | tpo3    | ecc..   |\n
        | DatetimeIndex | object  | object  | object  | object  |\n
        '''

        prepped_rates = self._prepare_rates(rates, decimal, tpo_size)
        tpo = self._from_prepared_rates_to_tpo(prepped_rates, tpo_size)
        prepped_rates.to_excel('./xlsx/prepped_rates.xlsx')
        tpo.to_excel('./xlsx/tpo.xlsx')
        return tpo

    def _prepare_rates(
            self, rates: List[Rates], decimal: int, tpo_size: int) -> DataFrame:
        '''
        Da rates: List[Rates] restituisce un DataFrame come segue

        | index         | open    | high    | low     | close   | tick_volume | spread | real_volume | thigh | tlow  |\n
        | DatetimeIndex | float64 | float64 | float64 | float64 | int64       | int64  | int64       | int64 | int64 |\n
        '''
        df = DataFrame(rates)
        df = df.set_index('time')
        df.to_excel('./xlsx/df.xlsx')
        # Errore se ci sono dei sabati / domeniche
        if _check_saturday_sunday(df):
            raise Exception('Ci sono dei sabati e delle domeniche')
        # transforma in tpo le colonne high e low
        df['thigh'] = self._df_column_float_to_tpo(
            df['high'], decimal, ceil, tpo_size)
        df['tlow'] = self._df_column_float_to_tpo(
            df['low'], decimal, floor, tpo_size)

        return df

    def _from_prepared_rates_to_tpo(
            self, prepped_rates: DataFrame, tpo_size: int) -> DataFrame:
        '''
        Da prepared_rates: DataFrame restituisce un DataFrame come segue

        | index         | tpo1    | tpo2    | tpo3    | ecc..   |\n
        | DatetimeIndex | object  | object  | object  | object  |\n
        '''
        high = prepped_rates['thigh'].max()
        low = prepped_rates['tlow'].min()
        rng = [x for x in range(low, high, tpo_size)]
        # crea e popola un nuovo dataframe usando il rng
        tpo = DataFrame(None,
                        columns=rng,
                        index=prepped_rates.index)
        # TODO si può ottimizzare probabilmente
        for row in prepped_rates.itertuples():
            tpo.loc[row.Index, row.tlow:row.thigh] = 'X'

        return tpo

    def _df_column_float_to_tpo(
            self, column: Series, decimal: int, round_func: Callable, tpo_size: int) -> Series:
        ser: Series
        # Arrotonda ad un numero intero
        ser = around(column * pow(10, decimal))
        # Arrotonda a tpo
        ser = round_func(ser / tpo_size) * tpo_size
        ser = ser.astype('int64')
        return ser
