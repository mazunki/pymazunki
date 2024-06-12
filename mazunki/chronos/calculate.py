#!/usr/bin/env python
import datetime as dt

from dataclasses import dataclass
import itertools
from typing import Self, Optional


@dataclass
class Time:
    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    label: Optional[str] = None

    @staticmethod
    def of(amount: int, name: str, /, label=None):
        if name in ("seconds", "second", "secs", "sec", "s"):
            return Time(seconds=amount, label=label)
        elif name in ("mins", "min"):
            return Time(minutes=amount, label=label)
        elif name in ("hours", "hour", "hrs", "hr", "h"):
            return Time(hours=amount, label=label)
        elif name in ("days", "day", "d"):
            return Time(days=amount, label=label)
        elif name in ("weeks", "week", "w", "wk"):
            return Time(weeks=amount, label=label)
        elif name in ("months", "mons", "mon"):
            return Time(months=amount, label=label)
        elif name in ("years", "year", "yr", "y"):
            return Time(years=amount, label=label)
        else:
            raise ValueError("{name} is not a valid time unit")

    @staticmethod
    def using(obj: dict[str, int]):
        t = Time()
        for unit, time in obj.items():
            t.__dict__[unit] = time
        return t

    @property
    def as_tuple(self):
        return (
            self.years,
            self.months,
            self.weeks,
            self.days,
            self.hours,
            self.minutes,
            self.seconds,
        )

    @property
    def as_dict(self) -> dict[str, int]:
        return {
            "years": self.years,
            "months": self.months,
            "weeks": self.weeks,
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds,
        }

    @property
    def as_timedelta(self):
        return dt.timedelta(
            # self.years,
            # self.months,
            # self.weeks,
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
        )

    def __repr__(self):
        values = [
            f"{key}={val}"
            for key, val in self.as_dict.items()
            if val != self.__class__.__dict__[key]
        ]
        return f"{self.__class__.__name__}({", ".join(values)})"

    def __str__(self):
        return self.__repr__()

    @property
    def in_future(self):
        return dt.datetime.now() + self.as_timedelta

    @property
    def in_past(self):
        return dt.datetime.now() - self.as_timedelta

    @classmethod
    def now(cls):
        return dt.datetime.now()

    def __neg__(self):
        return Time(**{k: -v for k, v in self.as_dict.items()})

    def __add__(self, other: Self):
        return Time.using(
            {
                "years": self.years + other.years,
                "months": self.months + other.months,
                "weeks": self.weeks + other.weeks,
                "days": self.days + other.days,
                "hours": self.hours + other.hours,
                "minutes": self.minutes + other.minutes,
                "seconds": self.seconds + other.seconds,
            }
        )

    def __sub__(self, other: Self):
        return Time.using(
            {
                "years": other.years - self.years,
                "months": other.months - self.months,
                "weeks": other.weeks - self.weeks,
                "days": other.days - self.days,
                "hours": other.hours - self.hours,
                "minutes": other.minutes - self.minutes,
                "seconds": other.seconds - self.seconds,
            }
        )

    def __hash__(self):
        return int("".join(map(str, self.as_tuple)))

    @staticmethod
    def parse(human_time: str) -> "Time":
        time_words = human_time.strip().lower().split(" ")

        match time_words:
            case ["today"]:
                return Time(label=human_time)
            case ["yesterday"]:
                return Time.of(1, "days")
            case ["tomorrow"]:
                return Time.of(1, "days")
            case *sometime, "ago":
                timeunits = {u: int(t) for t, u in itertools.batched(sometime, 2)}
                return -Time.using(timeunits)
            case "in", *sometime:
                timeunits = {u: int(t) for t, u in itertools.batched(sometime, 2)}
                return Time.using(timeunits)
            case _:
                raise ValueError(f"[error]: couldn't parse {time_words}")


#  vim: set sw=4 ts=4 expandtab
