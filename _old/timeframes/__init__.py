from MetaTrader5 import TIMEFRAME_D1, TIMEFRAME_H1, TIMEFRAME_H12, TIMEFRAME_H2, TIMEFRAME_H3, TIMEFRAME_H4, TIMEFRAME_H6, TIMEFRAME_H8, TIMEFRAME_M1, TIMEFRAME_M10, TIMEFRAME_M12, TIMEFRAME_M15, TIMEFRAME_M2, TIMEFRAME_M20, TIMEFRAME_M3, TIMEFRAME_M30, TIMEFRAME_M4, TIMEFRAME_M5, TIMEFRAME_M6, TIMEFRAME_M1, TIMEFRAME_W1


class ITimeframe:

    def __init__(self, name: str, const: int, value: int):
        self.name = name
        self.const = const
        self.value = value


class M1(ITimeframe):

    def __init__(self):
        super().__init__('M1', TIMEFRAME_M1, 1)


class M2(ITimeframe):

    def __init__(self):
        super().__init__('M2', TIMEFRAME_M2, 2)


class M3(ITimeframe):

    def __init__(self):
        super().__init__('M3', TIMEFRAME_M3, 3)


class M4(ITimeframe):

    def __init__(self):
        super().__init__('M4', TIMEFRAME_M4, 4)


class M5(ITimeframe):

    def __init__(self):
        super().__init__('M5', TIMEFRAME_M5, 5)


class M6(ITimeframe):

    def __init__(self):
        super().__init__('M6', TIMEFRAME_M6, 6)


class M10(ITimeframe):

    def __init__(self):
        super().__init__('M10', TIMEFRAME_M10, 10)


class M12(ITimeframe):

    def __init__(self):
        super().__init__('M12', TIMEFRAME_M12, 12)


class M15(ITimeframe):

    def __init__(self):
        super().__init__('M15', TIMEFRAME_M15, 15)


class M20(ITimeframe):

    def __init__(self):
        super().__init__('M20', TIMEFRAME_M20, 20)


class M30(ITimeframe):

    def __init__(self):
        super().__init__('M30', TIMEFRAME_M30, 30)


class H1(ITimeframe):

    def __init__(self):
        super().__init__('H1', TIMEFRAME_H1, 60)


class H2(ITimeframe):

    def __init__(self):
        super().__init__('H2', TIMEFRAME_H2, 120)


class H3(ITimeframe):

    def __init__(self):
        super().__init__('H3', TIMEFRAME_H3, 180)


class H4(ITimeframe):

    def __init__(self):
        super().__init__('H4', TIMEFRAME_H4, 240)


class H6(ITimeframe):

    def __init__(self):
        super().__init__('H6', TIMEFRAME_H6, 360)


class H8(ITimeframe):

    def __init__(self):
        super().__init__('H8', TIMEFRAME_H8, 480)


class H12(ITimeframe):

    def __init__(self):
        super().__init__('H12', TIMEFRAME_H12, 720)


class D1(ITimeframe):

    def __init__(self):
        super().__init__('D1', TIMEFRAME_D1, 1440)


class W1(ITimeframe):

    def __init__(self):
        super().__init__('W1', TIMEFRAME_W1, 10080)


class MON1(ITimeframe):

    def __init__(self):
        super().__init__('MON1', TIMEFRAME_MON1, 43200)


def Timeframe(timeframe_name: str) -> ITimeframe:
    cls = globals()[timeframe_name]
    return cls()
