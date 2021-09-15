from database import IDatabase, Param
from converter import IConverter
from adapter import IAdapter
from getter import IGetter, MTGetter
from rates import Rates
from profile_ import CreateProfile
from reference import Reference
from report import Report
from typing import Dict, List
from copy import deepcopy


class MarketScreen:
    """Classe che contiene tutti i Report di tutti i Symbol"""

    def __init__(self, g: IGetter, a: IAdapter, c: IConverter):
        self.__r = Rates(g, a, c)
        self.__dict_rep: Dict[str, Report] = {}

    def __getitem__(self, key: str) -> Report:
        return self.__dict_rep[key]

    def first_day_balance(self, db: IDatabase) -> None:
        """Calcola se il primo giorno e in balance per tutti i Symbols attivi"""

        active = db.get_active()

        for param in active:
            symbol = param.symbol
            # controll che non sia gi' stato calcolato
            try:
                calculated = self.__dict_rep[symbol][1][0].is_balance
            except:
                calculated = False

            if calculated is False:
                # calcola le rates per tutti i giorni ed il profilo principale
                rates = self.__r.get_rates(param)

                # crea profilo principale
                cp = CreateProfile()
                main_profile = cp.from_rates(rates, param.tpo_size)

                rep = Report(param, rates, main_profile)
                rep.first_day_balance()

                self.__dict_rep[param.symbol] = rep

    def get_balanced_days_only(self, frm: int, show_all: bool = False) -> List[str]:
        """Ritorna una lista con solo i giorni in Balance"""
        if show_all:
            return [key for (key, value) in self.__dict_rep.items()]
        else:
            l: List[str] = []
            for (key, value) in self.__dict_rep.items():
                # analizza solo il giorno specificato dal parametro frm
                rep = value[frm]
                found_one = False
                for ref in rep:
                    if ref.is_balance is True:
                        found_one = True
                if found_one is True:
                    l.append(key)
            return l

    def all_day_balance(self, param: Param) -> None:
        """Calcola il balance per tutti i giorni non ancora calcolato"""
        self.__dict_rep[param.symbol].all_day_balance(param)

    def find_reference_1(self, param: Param) -> None:
        """Calcola i reference point di reference1"""
        self.__dict_rep[param.symbol].find_reference_1()

    def find_reference_2(self, param: Param) -> None:
        """Calcola i reference point di reference2"""
        self.__dict_rep[param.symbol].find_reference_2()
