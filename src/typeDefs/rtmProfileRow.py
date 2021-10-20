import datetime as dt
from typing import TypedDict


class IRtmProfileRow(TypedDict):
    schDate: dt.datetime
    utilName: str
    rtmIexMu: float
    rtmPxiMu: float
    rtmBuyMu: float
    demMetMu: float
    demMetPerc: float
