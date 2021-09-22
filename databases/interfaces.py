from abc import ABC, abstractmethod
from typing import List
from databases.structs import Param


class IDatabase(ABC):
    """Interfaccia per collegamento e operazioni con il Database"""

    def __init__(self, dbinstance):
        self._db = dbinstance

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def add(self, param: Param) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> List[Param]:
        pass

    @abstractmethod
    def get(self, key: str) -> Param:
        pass

    @abstractmethod
    def update(self, param: Param) -> bool:
        pass

    @abstractmethod
    def remove(self, key: str) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
