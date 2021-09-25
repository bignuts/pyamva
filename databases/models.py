from typing import List
from typing_extensions import TypedDict

Param = TypedDict('Param', {'symbol': str, 'timeframe': int, 'days': int, 'decimal': int,
                  'offset': int, 'tpo_size': int, 'profiles': List[int], 'active': bool})

# class Param:
#     """Struttura per la definizione dei parametri"""

#     def __init__(self,
#                  symbol: str = '',
#                  timeframe: str = '',
#                  days: int = -1,
#                  decimal: int = -1,
#                  offset: int = -1,
#                  tpo_size: int = -1,
#                  profiles: List[int] = [],
#                  active: bool = False) -> None:

#         self.symbol = symbol
#         self.timeframe = timeframe
#         self.days = days
#         self.decimal = decimal    
#         self.offset = offset
#         self.tpo_size = tpo_size
#         self.profiles = profiles
#         self.active = active

# @classmethod
# def from_dict(cls, d: Dict):
#     symbol = d.get('symbol', '')
#     timeframe = d.get('timeframe', '')
#     days = d.get('days', -1)
#     decimal = d.get('decimal', -1)
#     offset = d.get('offset', -1)
#     tpo_size = d.get('tpo_size', -1)
#     profiles = d.get('profiles', [])
#     active = d.get('active', False)
#     return cls(symbol, timeframe, days, decimal, offset, tpo_size, profiles, active)

# def to_dict(self) -> Dict:
#     return {'symbol': self.symbol,
#             'timeframe': self.timeframe,
#             'days': self.days,
#             'decimal': self.decimal,
#             'offset': self.offset,
#             'tpo_size': self.tpo_size,
#             'profiles': self.profiles,
#             'active': self.active}

# def to_list(self) -> List:
#     return [self.symbol,
#             self.timeframe,
#             self.days,
#             self.decimal,
#             self.offset,
#             self.tpo_size,
#             self.profiles,
#             self.active]

# def __eq__(self, other):
#     if isinstance(other, self.__class__):
#         return self.__dict__ == other.__dict__
#     else:
#         return False
