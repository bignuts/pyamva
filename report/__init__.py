from typing import Dict, List, Union
from reference import Reference
import pandas as pd
from database import Param
from datetime import datetime

from util import TimeIt


class Report:
    """La classe report contine una List[List[Report]], essa contiene tutti i reference
    per tutti i giorni e profili impostati da paramentro"""

    def __init__(self, param: Param, rates: pd.DataFrame, main_profile: pd.DataFrame):
        self.__param = param
        self.__rates = rates
        self.__main_profile = main_profile

        self.__ref_list: List[List[Reference]] = []
        profiles = param.profiles
        # ordina crescente prima di uscar i valori all'interno
        profiles.sort()

        # calcola i diversi reference solo per l'ultimo giorno valido
        lst: List[Reference] = []
        for count in profiles:
            ref = Reference(rates, main_profile, param, 1, count)
            lst.append(ref)
        self.__ref_list.append(lst)

        # mapper = tuple(((start, count) for start in range(
        #     1, days-profiles[-1], 1) for count in profiles))

        # d, p = zip(*mapper)
        # from concurrent import futures
        # with futures.ThreadPoolExecutor() as executor:
        #     # submit work
        #     pool = executor.map(self.afunc, d, p)

        # def afunc(self, start: int, count: int) -> None:
        #     ref = Reference(self.main_profile, self.param, start, count)
        #     self.ref_list.append(ref)

    def __init_all_days(self, param: Param) -> None:
        """Serve per inizializzare tutti i giorni richiesti dai paramentri"""
        # aggiorna i paramentri nel caso siano da aggiornare
        self.__param = param

        days = self.__param.days
        profiles = self.__param.profiles
        # ordina crescente prima di uscar i valori all'interno
        profiles.sort()
        with TimeIt(self.__param.symbol):
            for start in range(1, days - profiles[-1], 1):
                lst: List[Reference] = []
                exist = self.__exist(start)
                if not exist:
                    for count in profiles:
                        pro = Reference(self.__rates,
                                        self.__main_profile,
                                        self.__param, start, count)
                        lst.append(pro)
                    self.__ref_list.append(lst)

    def __getitem__(self, key: Union[int, datetime]) -> List[Reference]:
        return self.__filter(self.__ref_list, key)

    def __filter(self, lst: List[List[Reference]], key: Union[int, datetime]) -> List[Reference]:
        """Ritorna da self.__ref_list: List[List[Reference]] l'indice corrispondete
        al giorno di inizio, List[Reference]"""
        if isinstance(key, int):
            for item in lst:
                if item[0].frm == key:
                    return item
        if isinstance(key, datetime):
            for item in lst:
                if item[0].end_time == key:
                    return item
        return []

    def __exist(self, key: int) -> bool:
        exist = self.__filter(self.__ref_list, key)
        if len(exist):
            return True
        return False

    def first_day_balance(self) -> None:
        """Trova balance solo per il primo giorno"""
        rl = self.__filter(self.__ref_list, 1)
        if rl is not None:
            for ref in rl:
                ref.find_balance()

    def all_day_balance(self, param: Param) -> None:
        """Trova balance per tutti i giorni non ancora calcolati"""
        self.__init_all_days(param)
        for ref in self.__ref_list:
            for days in ref:
                days.find_balance()

    def bracket_list(self) -> List[List]:
        """Ritorna una List[List] solo per i profili che hanno
        il primo giorno in lateralita"""
        lst1: List[List] = []
        for ref_grp in self.__ref_list:
            lst2: List = []
            lst2.append(ref_grp[0].end_time)
            lst2.append(int(ref_grp[0].vty))
            for ref in ref_grp:
                lst2.append(ref.balance_mod)
            lst1.append(lst2)
        return lst1

    def get_titles(self) -> List[str]:
        return [str(x) for x in self.__param.profiles]

    def find_reference_1(self) -> None:
        for ref in self.__ref_list:
            for days in ref:
                days.find_reference_1()

    def find_reference_2(self) -> None:
        for ref in self.__ref_list:
            for days in ref:
                days.find_reference_2()
