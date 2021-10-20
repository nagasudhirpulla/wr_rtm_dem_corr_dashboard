import datetime as dt
from src.config.appConfig import loadAppConfig
from src.app.getRtmProfileForDate import getRtmProfileForDate

nowDt = dt.datetime.now() - dt.timedelta(days=1)
appConf = loadAppConfig()

rtmProfileRows = getRtmProfileForDate(nowDt)

print("done")
