from connector.interfaces import IConnector
from metatrader5 import Initialize, Shutdown
from connector.interfaces import IConnector

# https://www.mql5.com/en/docs/integration/python_metatrader5

class MetaTrader(IConnector):

    def __init__(self):
        pass
