import datetime as dt
from src.app.getUtilsFromConfig import getUtilsFromConfig
from src.services.psp.getDemMetMuRows import getDemMetMuRows
from src.services.wbes.getSchForDate import getAllBuyerSchRowsForDate
from src.config.appConfig import getAppConfig
from src.typeDefs.rtmProfileRow import IRtmProfileRow
import pandas as pd


def getRtmProfileForDate(targetDt: dt.datetime) -> IRtmProfileRow:
    appConf = getAppConfig()

    # get the utilities name mappings info from app config
    utilsList = getUtilsFromConfig(appConf)
    wbesUtilToMainMapping = {}
    pspUtilToMainMapping = {}
    for u in utilsList:
        wbesUtilToMainMapping[u["wbesName"]] = u["utilName"]
        pspUtilToMainMapping[u["pspName"]] = u["utilName"]

    # get RTM data from wbes
    wbesBase = appConf["wbesBase"]
    schRows = getAllBuyerSchRowsForDate(targetDt, wbesBase, None)
    schRows = [x for x in schRows if ((x["schType"] in ["RTM_IEX", "RTM_PXI"]) and (
        x["utilName"] in list(wbesUtilToMainMapping.keys())))]

    for s in schRows:
        s["utilName"] = wbesUtilToMainMapping[s["utilName"]]

    # convert schedule rows as dataframe
    schDf = pd.DataFrame(schRows)
    schDf = schDf.groupby(
        ["utilName", "schDate", "schType"]).mean().reset_index()
    schDf = schDf.pivot(index=["utilName", "schDate"], columns=[
                        "schType"], values="val").reset_index()

    # get PSP data from db
    pspConnStr = appConf["pspConnStr"]
    pspFetchDt = targetDt
    if pspFetchDt.date() >= dt.datetime.now().date():
        pspFetchDt = dt.datetime.now() - dt.timedelta(days=1)
        pspFetchDt = dt.datetime(
            pspFetchDt.year, pspFetchDt.month, pspFetchDt.day)
    demMetMuRows = getDemMetMuRows(pspConnStr, pspFetchDt, pspFetchDt)
    demMetMuRows = [x for x in demMetMuRows if x["utilName"]
                    in list(pspUtilToMainMapping.keys())]

    for d in demMetMuRows:
        d["utilName"] = pspUtilToMainMapping[d["utilName"]]

    demMetDf = pd.DataFrame(demMetMuRows)
    demMetDf["schDate"] = targetDt

    # merge psp and wbes data to get rtm profile data for each state
    schDf = pd.merge(schDf, demMetDf, how="inner", on=["utilName", "schDate"])

    schDf["RTM_IEX"] = schDf["RTM_IEX"]*0.024

    schDf["RTM_PXI"] = schDf["RTM_PXI"]*0.024

    schDf["rtmBuyMu"] = schDf["RTM_IEX"]+schDf["RTM_PXI"]
    schDf["rtmBuyMu"][schDf["rtmBuyMu"] < 0] = 0

    schDf = schDf.rename(columns={"RTM_IEX": "rtmIexMu",
                                  "RTM_PXI": "rtmPxiMu"})

    schDf["demMetPerc"] = (100*schDf["rtmBuyMu"])/schDf["demMetMu"]
    rtmProfileRows = schDf.to_dict("records")

    return rtmProfileRows
