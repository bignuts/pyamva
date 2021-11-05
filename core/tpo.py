from typing import Callable, List, Tuple
from numpy import around, floor, ceil
from pandas import DataFrame, Series
from connectors.models import Rates
from datetime import datetime


def _check_saturday_sunday(rates_fd: DataFrame) -> bool:
    days = _days_in_df(rates_fd)
    # days.to_csv('./data/csv/days.csv')
    check_res = ((days['day_name'] == 'Saturday') |
                 (days['day_name'] == 'Sunday')).any()
    return check_res


def _days_in_df(rates_df: DataFrame) -> DataFrame:
    '''
    Il rates_df: Dataframe deve avere come indice un DatetimeIndex
    '''
    days = rates_df.resample('D').max()
    days = days.dropna(how='all')
    days['day_name'] = days.index.day_name()
    days['tz'] = days.index.tz
    return days[['day_name', 'tz']]

def _find_date(rates_df: DataFrame, frm: int, count: int) -> Tuple[datetime, datetime]:
    to = frm + count - 1
    days_df = _days_in_df(rates_df)
    return (days_df[frm], days_df[to])

# def slice_by_days(src_df: DataFrame, on: Optional[str], frm: int, count: int) -> DataFrame:
#     days = DataFrameUtil.find_date(src_df, on, frm, count)
#     if on is None:
#         dst_df = src_df[(src_df.index < days[0] + timedelta(days=1))
#                         & (src_df.index >= days[1])]
#         # dst_df = src_df[days[0] -
#         #                 timedelta(minutes=30)+timedelta(days=1):days[1]]  # type: ignore
#     else:
#         dst_df = src_df.loc[(src_df[on] < days[0] + timedelta(days=1))
#                             & (src_df[on] >= days[1])]
#     # TODO qui restituisce una copia di df non una view
#     return dst_df



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
        # prepped_rates.to_csv('./data/csv/prepped_rates.csv')
        # tpo.to_csv('./data/csv/tpo.csv')
        return tpo

    def _prepare_rates(
            self, rates: List[Rates], decimal: int, tpo_size: int) -> DataFrame:
        '''
        Da rates: List[Rates] restituisce un DataFrame come segue

        | index         | open    | high    | low     | close   | tick_volume | spread | real_volume | thigh | tlow  |\n
        | DatetimeIndex | float64 | float64 | float64 | float64 | int64       | int64  | int64       | int64 | int64 |\n
        '''
        rates_df = DataFrame(rates)
        rates_df = rates_df.set_index('time')
        # df.to_csv('./data/csv/df.csv')

        # Errore se ci sono dei sabati / domeniche
        if _check_saturday_sunday(rates_df):
            raise Exception('Ci sono dei sabati e delle domeniche')
        
        # transforma in tpo le colonne high e low
        rates_df['thigh'] = self._df_column_float_to_tpo(
            rates_df['high'], decimal, ceil, tpo_size)
        rates_df['tlow'] = self._df_column_float_to_tpo(
            rates_df['low'], decimal, floor, tpo_size)

        return rates_df

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

    # def from_bigger_tpo(self, main_profile: pd.DataFrame, frm: int, count: int) -> DataFrame:
    #     """Crea un Sub_Profile dal Main_Profile"""
    #     return slice_by_days(main_profile, None, frm, count).dropna(how='all', axis=1)
