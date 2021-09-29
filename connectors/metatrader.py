from datetime import datetime
from typing import Any, Union
from dotenv import dotenv_values
from connectors.interfaces import IConnector
from MetaTrader5 import initialize, shutdown, copy_rates_from, copy_rates_from_pos, copy_rates_range
from pandas import DataFrame, to_datetime


# https://www.mql5.com/en/docs/integration/python_metatrader5


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

    def get_rates(self, symbol: str, timeframe: int, frm: Union[int, datetime], to: Union[int, datetime]) -> DataFrame:
        """
        Parameters
        ----------
        frm : int, datetime
            frm è il parametro di inizio ricerca, il più vecchio cronologicamente

        to: int, datetime
            frm è il parametro di fine ricerca, il più recente cronologicamente

        Returns
        -------
        pandas.DataFrame -> Colonne |index|time:uint32|open:float64|high:float64|low:float64|close:float64|tick_volume:uint32|spread:uint32|real_volume:uint32|
        """
        rates: Any
        if type(frm) == datetime and type(to) == int:
            rates = copy_rates_from(symbol, timeframe, frm, to)
        if type(frm) == int and type(to) == int:
            rates = copy_rates_from_pos(symbol, timeframe, frm, to)
        if type(frm) == datetime and type(to) == datetime:
            rates = copy_rates_range(symbol, timeframe, frm, to)
        rates_df = DataFrame(rates)
        rates_df.index.name = 'index'
        rates_df = rates_df.astype({'time': 'uint32', 'tick_volume': 'uint32', # type: ignore
                        'spread': 'uint32', 'real_volume': 'uint32'}, errors='raise')
        # print(rates_df.dtypes)
        # converte time in formato datetime
        # rates_df['time']=to_datetime(rates_df['time'], unit='s')
        # inverte i dati, dal meno recente al più recente
        # rates_df = rates_df.iloc[::-1]
        return rates_df
