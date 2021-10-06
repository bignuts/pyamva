from typing_extensions import TypedDict
from datetime import datetime


Rates = TypedDict('Rates',
                  {'time': datetime,
                   'open': float,
                   'high': float,
                   'low': float,
                   'close': float,
                   'tick_volume': int,
                   'spread': int,
                   'real_volume': int})
