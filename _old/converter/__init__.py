import pandas as pd
from adapter import adp_rates
import abc


class IConverter:
    """Interfaccia per la trasformazione dei dati dell'interfaccia IAdapter a DataFrame"""

    @abc.abstractclassmethod
    def convert(self, rates: adp_rates) -> pd.DataFrame:
        pass


class MTConverter(IConverter):
    """Implementazione di IConverter, trasforma i dati da adp_rates a DataFrame"""
    # --------------------------------------------------------------------------------------------+
    # index | date           | open  | high  | low   | close | tick_volume | spread | real_volume |
    # int64 | datetime64[ns] | int64 | int64 | int64 | int64 | int64       | int64  | int64       |
    # ------+----------------+-------+-------+-------+-------+-------------+--------+-------------+
    #       |                |       |       |       |       |             |        |             |
    #       |                |       |       |       |       |             |        |             |
    #       |                |       |       |       |       |             |        |             |

    def convert(self, rates: adp_rates) -> pd.DataFrame:
        r = pd.DataFrame(rates,
                         columns=['date', 'open', 'high', 'low', 'close',
                                  'tick_volume', 'spread', 'real_volume'])
        # change index name
        r.index.name = 'index'
        return r


class DFConverter(IConverter):

    def convert(self, rates: pd.DataFrame) -> pd.DataFrame:
        rates.index.name = 'index'
        return rates
