from profile_ import CreateProfile
import pandas as pd
from typing import Dict, List, Optional, Tuple
from const import MINTPOCOUNT_010, MINTPOCOUNT_10P, MINTPOWIDTH, MINDAYBALANCE
from util import DataFrameUtil as DFU
from database import Param
from datetime import datetime


class Distribution:
    """Modello che si occupa di memorizzare i valori delle distribuzioni"""

    def __init__(self, low: int, high: int):
        self.ul = high
        self.uo: int
        self.uq: int
        self.mid: int
        self.lq: int
        self.lo: int
        self.ll = low

        self.__init()

    def __init(self) -> None:

        self.uo = int(self.ul - ((self.ul - self.ll)/8))
        self.uq = int(self.ul - ((self.ul - self.ll)/4))
        self.mid = int((self.ul + self.ll) / 2)
        self.lq = int(self.ll + ((self.ul - self.ll)/4))
        self.lo = int(self.ll + ((self.ul - self.ll)/8))


class Poc:

    def __init__(self, index: int, price: int, count: int) -> None:
        self.index = index
        self.price = price
        self.count = count


class ValueArea:

    def __init__(self, high: int, low: int):
        self.high = high
        self.low = low
        self.range = high - low


class Reference:
    """Classe per la computazione di tutti i Reference Point"""

    def __init__(self, rates: pd.DataFrame, main_profile: pd.DataFrame, param: Param, frm: int, count: int):
        cp = CreateProfile()

        # private
        self.__calc_balance = False

        # public

        # __init__
        self.param = param
        self.balance_mod = 'None'
        self.frm = frm
        self.count = count
        self.sub_profile = cp.from_main_profile(main_profile, frm, count)
        self.tpo_profile = self.__tpo_profile(self.sub_profile)

        # __references_from_rates
        self.__references_from_rates(
            DFU.slice_by_days(rates, 'date', frm, count))
        self.start_time: datetime
        self.end_time: datetime
        self.open: float
        self.high: float
        self.low: float
        self.close: float
        self.total_volume: int

        # find_balance
        self.is_balance: Optional[bool] = False

        # __init_distr
        self.distr: List[Distribution]

        # find_reference_1
        self.total_tpo: int
        self.vty: float

        # find_reference_2
        self.avarage_volume: float
        self.poc: Poc
        self.val: ValueArea

    def __references_from_rates(self, local_rates: pd.DataFrame) -> None:
        self.start_time = local_rates.iloc[-1, 0]
        self.end_time = local_rates.iloc[0, 0]
        self.open = local_rates.iloc[-1, 1]
        self.high = local_rates['high'].max()
        self.low = local_rates['low'].min()
        self.close = local_rates.iloc[0, 4]
        self.total_volume = local_rates['tick_volume'].sum()

    def find_reference_1(self) -> None:
        self.total_tpo = self.tpo_profile['count'].sum()
        self.vty = self.__vty(
            self.total_tpo, self.param.tpo_size, len(self.sub_profile.columns))

    def find_reference_2(self) -> None:
        self.avarage_volume = self.total_volume/self.count
        self.poc = self.__poc(self.tpo_profile)
        self.val = self.__val(self.tpo_profile, self.total_tpo*0.67, self.poc)

    def find_balance(self) -> None:
        """Calcola se il profilo è in una situazione di Balance o no,
        setta i parametri self.found_balance nel caso l'istanza ha
        gia eseguito questo metodo, self.is_balance = None se non ci
        sono abbastanza giorni per calcolarlo altrimenti True o False,
        self.balabce_mod indica se e in fase 'Bracket' o 'Alert trend'"""
        if self.__calc_balance is False:
            # calcola distribution
            self.distr, valid = self.__init_distr(
                self.tpo_profile, self.count, self.param.tpo_size)
            self.__calc_balance = True
            # verifica che sia in lateralita
            if self.count < MINDAYBALANCE or not valid:
                self.is_balance = None
            if len(self.distr) == 1 and self.count >= MINDAYBALANCE and valid:
                self.is_balance = True
            if len(self.distr) > 1 and self.count >= MINDAYBALANCE and valid:
                self.is_balance = False
            # se in lateralita valuta come
            if self.is_balance:
                if self.close >= self.distr[0].uo:
                    self.balance_mod = 'L Alert'
                if self.close > self.distr[0].mid and self.close < self.distr[0].uo:
                    self.balance_mod = 'Bracket L'
                if self.close <= self.distr[0].lo:
                    self.balance_mod = 'S Alert'
                if self.close < self.distr[0].mid and self.close > self.distr[0].lo:
                    self.balance_mod = 'Bracket S'
            elif self.count >= MINDAYBALANCE:
                self.balance_mod = 'Trending'

    def __tpo_profile(self, main_profile: pd.DataFrame) -> pd.DataFrame:
        """Calcola quanti tpo ci sono per ogni prezzo del main_profile, il profilo TPO appunto"""
        lista = []
        for c in main_profile.columns:
            lista.append((c, main_profile[c].count()))
        df = pd.DataFrame(lista, columns=['price', 'count'])
        df.index.name = 'index'
        # df = df[::-1] # reverse profile
        return df

    def __init_distr(self, tpo_count: pd.DataFrame, count: int, tpo_size: int) -> Tuple[List[Distribution], bool]:
        """Calcola le distribuzioni presenti nel profilo"""
        if count <= 10:
            minimum_tpo = MINTPOCOUNT_010
        else:
            minimum_tpo = MINTPOCOUNT_10P

        valid_tpo = tpo_count.loc[tpo_count['count'] >= minimum_tpo]

        # TODO qui ci vorrebbe un controllo nel caso valid_tpo non fosse valido
        if len(valid_tpo):
            mask = valid_tpo['price'].diff() > tpo_size

            last_index = valid_tpo.index[0]

            distr_list = []

            for index, price, count in valid_tpo[mask].itertuples():
                distr = valid_tpo.loc[last_index:index - 1]
                if len(distr) > MINTPOWIDTH:
                    d = Distribution(distr.iloc[0, 0], distr.iloc[-1, 0])
                    distr_list.append(d)
                last_index = index

            distr = valid_tpo.loc[last_index:valid_tpo.index[-1]]
            if len(distr) > MINTPOWIDTH:
                d = Distribution(distr.iloc[0, 0], distr.iloc[-1, 0])
                distr_list.append(d)

            return distr_list, True

        print(
            f'{self.param.symbol} metodo __init_distr non ha trovato nessun valid_tpo, l ultima volta era legato ad un problema con gli offset e dst, vedi DateTimeUtil.utc_add_offset')
        return [Distribution(0, 0)], False

    def __vty(self, total_tpo: int, tpo_size: int, tpo_occur: int) -> float:
        """Calcola vty nel profilo"""
        return (total_tpo * tpo_size) / tpo_occur

    def __poc(self, tpo_profile: pd.DataFrame) -> Poc:
        """Calcola poc nel profilo"""
        # massimo numero di tpo
        max_count = tpo_profile['count'].max()
        # ritorna DataFrame con tutti i valori di max_count
        poc_df = tpo_profile.loc[tpo_profile['count'] == max_count]

        if len(poc_df) > 1:
            # trova il valore in mezzo al profilo
            mid_tpo_profile = int(len(tpo_profile)/2)
            # sottrazzione per individuare quale dei vari tpo e piu centrato
            poc_df['diff'] = abs(mid_tpo_profile - poc_df.index)
            # valore minore di diff
            min_diff = poc_df['diff'].min()
            # indice corrispondente
            index_diff = poc_df.loc[poc_df['diff'] == min_diff].index
            poc_df = tpo_profile.iloc[index_diff]

        return Poc(poc_df.index.values[0], poc_df['price'].values[0], poc_df['count'].values[0])

    def __val(self, tpo_profile: pd.DataFrame, target: float, poc: Poc) -> ValueArea:
        """Calcola value area nel profilo"""
        poc_index = poc.index
        upper_index = [poc_index, poc_index + 2]
        lower_index = [poc_index, poc_index - 2]

        tpo_sum = poc.count
        last_sum_flag = ''

        while tpo_sum < target:

            upper_df = tpo_profile.iloc[upper_index[0]+1:upper_index[1]+1, 1]
            lower_df = tpo_profile.iloc[lower_index[1]:lower_index[0], 1]
            upper_sum = upper_df.sum()
            lower_sum = lower_df.sum()

            if upper_sum > lower_sum:
                tpo_sum += upper_sum
                upper_index[0] = upper_index[0] + 2
                upper_index[1] = upper_index[1] + 2
                last_sum_flag = 'U'
            if lower_sum > upper_sum:
                tpo_sum += lower_sum
                lower_index[0] = lower_index[0] - 2
                lower_index[1] = lower_index[1] - 2
                last_sum_flag = 'D'
            if upper_sum == lower_sum:
                i = 1
                while True:
                    new_upper_df = tpo_profile.iloc[upper_index[0] +
                                                    2*1+1:upper_index[1]+2*i+1, 1]
                    new_lower_df = tpo_profile.iloc[lower_index[1] -
                                                    2*i:lower_index[0]-2*i, 1]
                    new_upper_sum = new_upper_df.sum()
                    new_lower_sum = new_lower_df.sum()
                    if new_upper_sum > new_lower_sum:
                        tpo_sum += upper_sum
                        upper_index[0] = upper_index[0] + 2
                        upper_index[1] = upper_index[1] + 2
                        last_sum_flag = 'U'
                        break
                    if new_lower_sum > new_upper_sum:
                        tpo_sum += lower_sum
                        lower_index[0] = lower_index[0] - 2
                        lower_index[1] = lower_index[1] - 2
                        last_sum_flag = 'D'
                        break
                    if upper_sum == lower_sum:
                        i += 1

        # controlla se e possibile togliere l'ultima somma
        if last_sum_flag == 'U':
            partial_df = tpo_profile.iloc[lower_index[0]:upper_index[0], 1]
            partial_sum = partial_df.sum()
            if partial_sum > target:
                high = tpo_profile.iloc[upper_index[0]-1, 0]
                low = tpo_profile.iloc[lower_index[0], 0]
                return ValueArea(high, low)
        if last_sum_flag == 'D':
            partial_df = tpo_profile.iloc[lower_index[0]+1:upper_index[0]+1, 1]
            partial_sum = partial_df.sum()
            if partial_sum > target:
                high = tpo_profile.iloc[upper_index[0], 0]
                low = tpo_profile.iloc[lower_index[0]+1, 0]
                return ValueArea(high, low)

        # iloc[row, col]
        high = tpo_profile.iloc[upper_index[0], 0]
        low = tpo_profile.iloc[lower_index[0], 0]
        return ValueArea(high, low)
