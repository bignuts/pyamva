import pandas as pd
import abc
from typing import Tuple
from numpy import ndarray
from datetime import datetime
from pytz import timezone
from util import DateTimeUtil as DTU


adp_rates = Tuple[Tuple[datetime, int, int, int, int, int, int, int]]


class IAdapter:
    """Interfaccia per la trasformazione/preparazione dei dati dell'interfaccia IGetter,
    per poi passarli all'interfaccia IConverter"""

    @abc.abstractclassmethod
    def adapt(self, rates, decimal: int, offset: int) -> adp_rates:
        pass

    def _float_to_int(self, num: float, decimal: int) -> int:
        return round(num*pow(10, decimal))


class MTAdapter(IAdapter):
    """Implementazione dell'interfaccia IAdapter, transforma i data da mt_rates a adp_rates"""

    def __init__(self):
        super().__init__()

    def adapt(self, rates: ndarray, decimal: int, offset: int) -> adp_rates:
        # df = pd.DataFrame()
        l = []
        for rate in rates:
            # convertire time in datetime
            # time = rate[0]
            time = datetime.utcfromtimestamp(rate[0])
            # si aggiusta l'orario in base all'offset
            utc_offset = self._convert_time(time, offset)
            l.append((utc_offset, self._float_to_int(rate[1], decimal), self._float_to_int(rate[2], decimal), self._float_to_int(
                rate[3], decimal), self._float_to_int(rate[4], decimal), int(rate[5]), int(rate[6]), int(rate[7])))
        return tuple(l)  # type: ignore

    def _convert_time(self, date: datetime, offset: int) -> datetime:
        utc_date = DTU.naive_to_utc(date)
        if offset != 0:
            utc_offset = DTU.utc_add_offset(utc_date, offset)
        else:
            utc_offset = utc_date

        return utc_offset


class DFAdapter(IAdapter):

    def adapt(self, rates: pd.DataFrame, decimal: int = 0, offset: int = 0) -> pd.DataFrame:
        return rates
