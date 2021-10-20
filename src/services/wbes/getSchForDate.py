import datetime as dt
from typing import List, Optional
import requests
import re
import json
from src.services.wbes.getMaxRev import getMaxRevForDate
from src.services.wbes.wbesUtils import getDefaultReqHeaders
from src.typeDefs.wbes.schDataRow import ISchDataRow

def convertDataArrayToSchRows(dataArray: List[List[str]], targetDt: dt.datetime) -> List[ISchDataRow]:
    dataRows = []
    # check for the dimension of dataArray
    if len(dataArray) != 102:
        return []
    if len(dataArray[0]) < 3:
        return []
    for blk in range(1, 97):
        rowNum = blk + 1
        for colIter in range(2, len(dataArray[0])-1):
            genName = dataArray[0][colIter]
            schType = dataArray[1][colIter]
            schVal = dataArray[rowNum][colIter]
            dataRows.append({
                'utilName': genName,
                'schDate': dt.datetime(targetDt.year, targetDt.month, targetDt.day),
                'block': blk,
                'schType': schType,
                'val': float(schVal)
            })
    return dataRows


def getAllBuyerSchRowsForDate(targetDt: dt.datetime, wbesBase: str, revNum: Optional[int] = None) -> List[ISchDataRow]:
    rev = revNum
    # get max rev of day if rev number not specified
    if revNum == None:
        rev = getMaxRevForDate(targetDt, wbesBase)
    headers = getDefaultReqHeaders()
    schUrl = "{0}/ReportNetSchedule/GetNetScheduleSummary?regionId=2&scheduleDate={1}&sellerId=ALL&revisionNumber={2}&byDetails=1&isBuyer=1".format(
        wbesBase, dt.datetime.strftime(targetDt, '%d-%m-%Y'), rev)
    r = requests.get(schUrl, headers=headers, verify=False)
    resText = r.text
    # extract data array from the response
    jsonText = re.search('var data = JSON.parse\((.*)\);', resText).group(1)
    jsonText = jsonText.replace("\\", "")
    dataArray = json.loads(jsonText[1:-1])
    dataRows = convertDataArrayToSchRows(dataArray, targetDt)
    return dataRows
