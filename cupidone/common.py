from datetime import date, datetime, time, timedelta


def dt_to_iso(value: datetime):
    return value.isoformat(sep="T", timespec="seconds")


def iso_to_dt(value: str):
    return datetime.fromisoformat(value)


def dt_to_ymd(value: datetime):
    return date_to_yms(value.date())


def date_to_yms(value: date):
    return f"{value.year:04d}-{value.month:02d}-{value.day:02d}"


def iso_to_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def reduce_actions(reducer, actions, initial_state = None):
    state = initial_state
    for action in actions:
        state = reducer(state, action)
    return state


class State():
    def __init__(self, value=None):
        self.value = value

def int_to_time(value: int) -> time:
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time(hour=hours, minute=minutes, second=seconds)


def int_to_timedelta(value: int) -> timedelta:
    return timedelta(seconds=value)


def int_to_hms(value: int):
    sign = ""
    if value < 0:
        value = -1 * value
        sign = "-"
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"


def time_to_hms(value: time):
    seconds = value.hour * 3600 + value.minute * 60 + value.second
    return int_to_hms(seconds)


def timedelta_to_hms(value: timedelta):
    seconds = value.seconds + 24 * 60 * 60 * value.days
    return int_to_hms(seconds)


def normalize(values):
    result = [*values]
    count = len(values)
    zero = "0"
    if count == 1:
        result.append(zero)
        result.append(zero)
        return result
    if count == 2:
        for i in range(count):
            if result[i] == "":
                result[i] = zero
        result.append(zero)
        return result
    if count == 3:
        for i in range(count):
            if result[i] == "":
                result[i] = zero
        return result
    raise ValueError()


def hms_to_int(value: str):
    [h, m, s] = normalize(value.split(":"))
    hours = int(h) * 3600
    minutes = int(m) * 60
    seconds = int(s)
    return hours + minutes + seconds


def hms_to_time(value: str):
    total_seconds = hms_to_int(value)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time(hour=hours, minute=minutes, second=seconds)


def value_decorator(f):
    def wrap(*args, **kwargs):
        return f(*args, **kwargs).value
    return wrap


app_name = "cupidone"
app_version = "0.2.0"
output_dir = "todo"

legend = [
    "🔵 - backlog",
    "⚪ - to do",
    "🟡 - in progress",
    "🟢 - done",
    "⭕ - outdated"
]

state_emojies_map = {
    "backlog": "🔵",
    "todo": "⚪",
    "in progress": "🟡",
    "done": "🟢",
    "outdated": "⭕"
}


class BaseConverter():
    def __init__(self):
        pass

    def read(filename:str) -> None:
        pass

    def write() -> None:
        pass


__all__ = [
    "app_name",
    "app_version",
    "output_dir",
    "legend",
    "state_emojies_map"
]
