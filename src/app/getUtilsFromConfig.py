from typing import List
from src.config.appConfig import loadAppConfig
from src.typeDefs.utilInfo import IUtilInfo


def getUtilsFromConfig(appConf) -> List[IUtilInfo]:
    confUtils = appConf["utils"]
    utilsList: List[IUtilInfo] = []
    for cU in confUtils:
        utilObj: IUtilInfo = {
            "utilName": cU[0],
            "wbesName": cU[1],
            "pspName": cU[2]
        }
        utilsList.append(utilObj)
    return utilsList
