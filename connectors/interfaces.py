from abc import ABC, abstractmethod
from typing import List, Union
from datetime import datetime
from .models import Rates


class IConnector(ABC):
    """
    Interfaccia per l'acquisizione dei dati
    """

    @abstractmethod
    def _connect(self) -> None:
        pass

    @abstractmethod
    def _disconnect(self) -> None:
        pass

    @abstractmethod
    def get_rates(self, symbol: str, timeframe: int,
                  frm: Union[int, datetime], to: Union[int, datetime]) -> List[Rates]:
        pass
