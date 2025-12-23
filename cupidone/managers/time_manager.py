import abc
from datetime import datetime, date, time


class AbstractTimeManager(abc.ABC):
    @abc.abstractmethod
    def get_time(self) -> time:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_date(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_datetime(self) -> datetime:
        raise NotImplementedError()

    @abc.abstractmethod
    def merge_time(self, time: time) -> datetime:
        raise NotImplementedError()

    @abc.abstractmethod
    def merge_date(self, date: date) -> datetime:
        raise NotImplementedError()


class TimeManager(AbstractTimeManager):
    def __init__(self, tz_name: str = None, tz_offset: int = None):
        self.timezone = None
        # self.timezone = datetime.now().astimezone().tzinfo
        # if tz_name and tz_offset:
        #     self.timezone = timezone(name=tz_name, offset=timedelta(seconds=tz_offset))

    def get_time(self) -> time:
        return self.get_datetime().time()

    def get_date(self) -> date:
        return self.get_datetime().date()

    def get_datetime(self) -> datetime:
        return datetime.now(tz=self.timezone).replace(microsecond=0)

    def merge_time(self, time: time) -> datetime:
        now = self.get_datetime()
        return datetime.combine(date=now.date(), time=time, tzinfo=self.timezone)

    def merge_date(self, date: date) -> datetime:
        now = self.get_datetime()
        return datetime.combine(date=date, time=now.time(), tzinfo=self.timezone)

    def merge_date_time(self, date: date, time: time) -> datetime:
        return datetime.combine(date=date, time=time, tzinfo=self.timezone)


__all__ = ["TimeManager"]
