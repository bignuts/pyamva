from datetime import datetime, timedelta, timezone
from typing import List, Union
from zoneinfo import ZoneInfo
from dotenv import dotenv_values
from .interfaces import IConnector
from MetaTrader5 import initialize, shutdown, copy_rates_from, copy_rates_from_pos, copy_rates_range
from .models import Rates
from numpy import ndarray


# https://www.mql5.com/en/docs/integration/python_metatrader5
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

class MetaTrader(IConnector):
    """
    Implementazione di IConnector per acquisizione dati da MetaTrader5.
    """

    def __init__(self):
        self._connect()

    def __del__(self):
        self._disconnect()

    def _connect(self) -> None:
        env = dotenv_values(".env")
        initialize(login=int(env['MT5_USER']),  # type: ignore
                   password=env['MT5_PASS'],
                   server=env['MT5_SERVER'])

    def _disconnect(self) -> None:
        shutdown()

    def get_rates(self,
                  symbol: str,
                  timeframe: int,
                  frm: Union[int,
                             datetime],
                  to: Union[int,
                            datetime]) -> List[Rates]:
        """
        Parameters
        ----------
        frm : int, datetime
            frm è il parametro di inizio ricerca, il più vecchio cronologicamente

        to: int, datetime
            to è il parametro di fine ricerca, il più recente cronologicamente
        """

        rates_list: List[Rates] = []

        if isinstance(frm, datetime) and isinstance(to, int):
            rates = copy_rates_from(symbol, timeframe, frm, to)
        if isinstance(frm, int) and isinstance(to, int):
            rates = copy_rates_from_pos(symbol, timeframe, frm, to)
        if isinstance(frm, datetime) and isinstance(to, datetime):
            rates = copy_rates_range(symbol, timeframe, frm, to)

        for rate in rates:
            transformed_rates = self._transform_rates(rate)
            rates_list.append(transformed_rates)
        return rates_list

    def _transform_rates(self, rate: ndarray) -> Rates:
        epoch = rate[0]
        # epoch = self._add_hours_to_epoch(rate[0], 1)
        # time = datetime.utcfromtimestamp(epoch)
        time = datetime.fromtimestamp(epoch)
        # time = datetime.utcfromtimestamp(epoch).astimezone(timezone.utc)
        # time = datetime.fromtimestamp(epoch, tz=ZoneInfo('Europe/Rome'))
        # time = datetime.fromtimestamp(epoch, tz=ZoneInfo('America/New_York'))
        open = float(rate[1])
        high = float(rate[2])
        low = float(rate[3])
        close = float(rate[4])
        tick_volume = int(rate[5])
        spread = int(rate[6])
        real_volume = int(rate[7])
        rate_dict = Rates(
            time=time,
            open=open,
            high=high,
            low=low,
            close=close,
            tick_volume=tick_volume,
            spread=spread,
            real_volume=real_volume)
        return rate_dict

    def _add_hours_to_epoch(self, epoch: int, hours: int) -> int:
        return epoch + (60 * 60 * hours)
