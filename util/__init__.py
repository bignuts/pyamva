from time import time
from pandas import DataFrame, Series
from datetime import datetime, timedelta
from math import floor
from typing import Optional, Tuple, List, Dict
from zoneinfo import ZoneInfo


def list_to_str(lst: List) -> str:
    return ', '.join(str(i) for i in lst)


def str_to_list(s: str) -> List[int]:
    res = s.split(',')
    return list(map(int, res))


def str_to_bool(s: str) -> bool:
    if s == 'False':
        return False
    else:
        return True


class DataFrameUtil:

    @staticmethod
    def days_in_df(src_df: DataFrame, on: Optional[str]) -> Series:
        # resample e restituisce i giorni nel df e lo inverte
        dst_df = src_df.resample('D', on=on).max().iloc[::-1]
        # aggiunge colonna con il nome della settimana
        # df['day_of_week'] = df['date'].dt.day_name()
        # df.to_csv('series.csv')
        # rimuove le righe cha hanno valori vuote
        dst_df = dst_df.dropna(how='all')
        # converte DateTimeIndex in series
        dst_df = dst_df.index.to_series(
            index=[i for i in range(len(dst_df))], keep_tz=True)
        return dst_df

    @staticmethod
    def find_date(src_df: DataFrame, on: Optional[str], frm: int, count: int) -> Tuple[datetime, datetime]:
        to = frm + count - 1
        dst_df = DataFrameUtil.days_in_df(src_df, on)
        return (dst_df[frm], dst_df[to])

    @staticmethod
    def slice_by_days(src_df: DataFrame, on: Optional[str], frm: int, count: int) -> DataFrame:
        days = DataFrameUtil.find_date(src_df, on, frm, count)
        if on is None:
            dst_df = src_df[(src_df.index < days[0] + timedelta(days=1))
                            & (src_df.index >= days[1])]
            # dst_df = src_df[days[0] -
            #                 timedelta(minutes=30)+timedelta(days=1):days[1]]  # type: ignore
        else:
            dst_df = src_df.loc[(src_df[on] < days[0] + timedelta(days=1))
                                & (src_df[on] >= days[1])]
        # TODO qui restituisce una copia di df non una view
        return dst_df


class DateTimeUtil:

    @staticmethod
    def naive_to_utc(date: datetime) -> datetime:
        # utc = pytz.utc
        # return utc.localize(date)
        return date.replace(tzinfo=ZoneInfo('UTC'))

    @staticmethod
    def naive_to_local(date: datetime) -> datetime:
        # local = tzlocal.get_localzone()
        # return local.localize(date)
        return date.replace(tzinfo=ZoneInfo('localtime'))

    @staticmethod
    def naive_local_to_utc(date: datetime) -> datetime:
        DTU = DateTimeUtil.naive_to_local(date)
        return DateTimeUtil.local_to_utc(DTU)

    @staticmethod
    def utc_now() -> datetime:
        return DateTimeUtil.naive_to_utc(datetime.utcnow())

    @staticmethod
    def local_now() -> datetime:
        return DateTimeUtil.naive_to_local(datetime.now())

    @staticmethod
    def local_to_utc(date: datetime) -> datetime:
        # return date.astimezone(pytz.utc)
        return date.astimezone(ZoneInfo('UTC'))

    @staticmethod
    def utc_to_local(date: datetime) -> datetime:
        # return date.astimezone(tzlocal.get_localzone())
        return date.astimezone(ZoneInfo('localtime'))

    @staticmethod
    def utc_add_offset(date: datetime, offset: int) -> datetime:
        # non so perche ma bisogna cambiare il segno
        # Italy has only 1 time zone. Central European Time (CET) is used as standard time, while Central European Summer Time (CEST) is observed when Daylight Saving Time (DST) is in force.
        # offset-1 quando il dst non è attivo, offset-0 quando dst è attivo

        offset = offset * -1
        if offset < 0:
            off = f'{offset}'
        if offset >= 0:
            off = f'+{offset}'
        # return date.astimezone(pytz.timezone(f'Etc/GMT{off}'))
        return date.astimezone(ZoneInfo(f'Etc/GMT{off}'))

    @staticmethod
    def date_round(date: datetime) -> datetime:
        return datetime(date.year, date.month, date.day, tzinfo=date.tzinfo)


class TimeIt:

    def __init__(self, caller: str):
        self.__start = None
        self.__caller = caller

    def __enter__(self):
        self.__start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'Total time taken: {self.duration()}')

    def duration(self):
        time_ = time() - self.__start
        minutes = floor(time_/60)
        seconds = time_ % 60
        return (f'({self.__caller}) {minutes} min: {seconds} sec')
