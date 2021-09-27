from abc import ABC, abstractmethod
from typing import Dict, Optional, Sequence, List


class IDatabase(ABC):
    '''Interfaccia per collegamento e operazioni con il dabase'''

    @abstractmethod
    def connect(self, db_path: str) -> None:
        '''Metodo per connettersi al database e restituisce un'istanza ad esso'''
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def select_table(self, table_name: str) -> None:
        pass

    @abstractmethod
    def add(self, record: Dict) -> int:
        pass

    @abstractmethod
    def get_all(self) -> Sequence[Dict]:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[Dict]:
        pass

    @abstractmethod
    def remove(self, id: List[int]) -> List[int]:
        pass

    @abstractmethod
    def update(self, id: List[int], fields) -> List[int]:
        pass
