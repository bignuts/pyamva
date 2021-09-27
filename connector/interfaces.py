from abc import ABC, abstractclassmethod
from typing import Union
from datetime import datetime
from typing_extensions import ParamSpecArgs


class IConnector(ABC):
    """Interfaccia per l'acquisizione dei dati"""

    @abstractclassmethod
    def connect(self):
        pass

    @abstractclassmethod
    def disconnect(self):
        pass

    @abstractclassmethod
    def get_rates(self, symbol: str, timeframe: int, frm: Union[int, datetime], to: Union[int, datetime]):
        pass
