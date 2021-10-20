import datetime as dt
from typing import TypedDict


class IDemMetMuRow(TypedDict):
    utilName: str
    schDate: dt.datetime
    demMetMu: float
