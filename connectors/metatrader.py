from datetime import datetime
from typing import Union
from dotenv import dotenv_values
from connectors.interfaces import IConnector
from MetaTrader5 import initialize, shutdown


# https://www.mql5.com/en/docs/integration/python_metatrader5


class MetaTrader(IConnector):

    def __init__(self):
        self._connect()

    def __del__(self):
        self._disconnect()

    def _connect(self) -> None:
        env = dotenv_values(".env")
        initialize(login=int(env['MT5_USER']), # type: ignore
                   password=env['MT5_PASS'], 
                   server=env['MT5_SERVER'])

    def _disconnect(self) -> None:
        shutdown()

    def get_rates(self, symbol: str, timeframe: int, frm: Union[int, datetime], to: Union[int, datetime]):
        return super().get_rates(symbol, timeframe, frm, to)
