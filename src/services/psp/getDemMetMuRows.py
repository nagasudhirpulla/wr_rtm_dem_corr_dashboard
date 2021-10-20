# TODO complete this
from typing import List
import cx_Oracle
import datetime as dt
from src.typeDefs.psp.demMetMuRow import IDemMetMuRow


def getDemMetMuRows(connStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IDemMetMuRow]:
    demMetRows: List[IDemMetMuRow] = []
    # create a connection object
    conn = cx_Oracle.connect(connStr)

    # get a cursor object from the connection
    cur = conn.cursor()

    try:
        # create sql for querying data
        sqlTxt = "SELECT date_key, availability, state_name FROM REPORTING_UAT.state_load_details \
                    where date_key between :2 and :3 order by date_key"
        startDtKey = dt.datetime.strftime(startDt, "%Y%m%d")
        endDtKey = dt.datetime.strftime(endDt, "%Y%m%d")
        # execute the sql to perform data extraction
        cur.execute(sqlTxt, (startDtKey, endDtKey))

        # get the column names returned from the query
        # colNames = [row[0] for row in cur.description]

        # fetch all rows from query
        dbRows = cur.fetchall()
        for r in dbRows:
            demRow: IDemMetMuRow = {
                "utilName": r[2],
                "schDate": dt.datetime.strptime(str(r[0]), "%Y%m%d"),
                "demMetMu": r[1]
            }
            demMetRows.append(demRow)
    except Exception as err:
        print('Error while querying data from db')
        print(err)
    finally:
        # closing database cursor and connection
        if cur is not None:
            cur.close()
        conn.close()
    return demMetRows
