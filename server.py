from src.config.appConfig import loadAppConfig
from flask import Flask, render_template, request
import datetime as dt
from src.app.getRtmProfileForDate import getRtmProfileForDate

app = Flask(__name__)

# get application config
appConf = loadAppConfig()

# Set the secret key to some random bytes
app.secret_key = appConf['flaskSecret']


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        return render_template('home.html.j2', data={"startDt": (dt.datetime.now()-dt.timedelta(days=1)).strftime("%Y-%m-%d")})
    else:
        startDtStr = request.form.get('startDate')
        startDt = dt.datetime.strptime(startDtStr, '%Y-%m-%d')
        rtmProfileRows = getRtmProfileForDate(startDt)
        for rItr in range(len(rtmProfileRows)):
            rtmProfileRows[rItr]["rtmIexMu"] = round(
                rtmProfileRows[rItr]["rtmIexMu"], 2)
            rtmProfileRows[rItr]["rtmPxiMu"] = round(
                rtmProfileRows[rItr]["rtmPxiMu"], 2)
            rtmProfileRows[rItr]["rtmBuyMu"] = round(
                rtmProfileRows[rItr]["rtmBuyMu"], 2)
            rtmProfileRows[rItr]["demMetMu"] = round(
                rtmProfileRows[rItr]["demMetMu"], 2)
            rtmProfileRows[rItr]["demMetPerc"] = round(
                rtmProfileRows[rItr]["demMetPerc"], 2)
        return render_template('home.html.j2', data={"startDt": startDt.strftime("%Y-%m-%d"), "rtm": rtmProfileRows})


if __name__ == '__main__':
    srvMode = appConf["mode"]
    app.run(host="0.0.0.0", port=int(
        appConf['flaskPort']), debug=True if srvMode == "d" else False)
