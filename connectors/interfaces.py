from abc import ABC, abstractclassmethod
from typing import Union
from datetime import datetime


class IConnector(ABC):
    """Interfaccia per l'acquisizione dei dati"""

    @abstractclassmethod
    def _connect(self) -> None:
        pass

    @abstractclassmethod
    def _disconnect(self) -> None:
        pass

    @abstractclassmethod
    def get_rates(self, symbol: str, timeframe: int, frm: Union[int, datetime], to: Union[int, datetime]):
        pass
