import datetime as dt
from typing import TypedDict


class ISchDataRow(TypedDict):
    utilName: str
    schDate: dt.datetime
    block: int
    schType: str
    val: float
