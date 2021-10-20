import datetime as dt
import requests
from src.services.wbes.wbesUtils import getDefaultReqHeaders


def getMaxRevForDate(revDt: dt.datetime, wbesBase: str):
    headers = getDefaultReqHeaders()
    revUrl = "{0}/Report/GetCurrentDayFullScheduleMaxRev?regionid=2&ScheduleDate={1}".format(
        wbesBase, dt.datetime.strftime(revDt, "%d-%m-%Y"))
    r = requests.get(revUrl, headers=headers, verify=False)
    maxRevObj = r.json()
    return maxRevObj['MaxRevision']
