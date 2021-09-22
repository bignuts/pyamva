import pandas as pd
# from MetaTrader5 import MT5Initialize, MT5Shutdown, MT5TerminalInfo, MT5WaitForTerminal, MT5CopyRatesFrom, MT5CopyRatesFromPos, MT5CopyRatesRange, MT5Rate
from MetaTrader5 import initialize, shutdown, terminal_info, copy_rates_range, copy_rates_from, copy_rates_from_pos
from typing import Tuple, Union
from datetime import datetime
import abc
from timeframes import ITimeframe
from numpy import ndarray


class IGetter:
    """Interfaccia per l'acquisizione dei dati"""

    @abc.abstractclassmethod
    def get_rates(self, symbol: str, timeframe: ITimeframe, frm, to):
        pass


class MTGetter(IGetter):
    """Implementazione di IGetter, usa MT5 per acquisizione dati"""

    def __init__(self):
        self._connect()

    def __del__(self):
        shutdown()

    def _connect(self, path: str = '') -> None:
        if not initialize(path):
            print('Connection to MetaTrader Failed!')

    def get_rates(self, symbol: str, timeframe: ITimeframe, frm: Union[int, datetime], to: Union[int, datetime]) -> ndarray:
        if terminal_info().connected:
            if type(frm) == datetime and type(to) == datetime:
                r = copy_rates_range(symbol, timeframe.const, frm, to)
            if type(frm) == datetime and type(to) == int:
                r = copy_rates_from(symbol, timeframe.const, frm, to)
            if type(frm) == int and type(to) == int:
                r = copy_rates_from_pos(symbol, timeframe.const, frm, to)
            # Inverto tuple, il primo elemento è il rate più recente
            r = r[::-1]
            return r
        else:
            print('Not Connected to MetaTrader')
        return (ndarray, )


class DFGetter(IGetter):

    def get_rates(self, symbol: str, timeframe: ITimeframe, frm: Union[int, datetime], to: Union[int, datetime]) -> pd.DataFrame:

        df = pd.read_csv(symbol+'.csv', index_col=0)
        # cambia tipo
        df['date'] = pd.to_datetime(df['date'])

        if type(frm) == datetime and type(to) == datetime:
            return df.loc[(df['date'] > frm) & (df['date'] <= to)]
        if type(frm) == int and type(to) == int:
            return df.iloc[frm:to]  # type: ignore
