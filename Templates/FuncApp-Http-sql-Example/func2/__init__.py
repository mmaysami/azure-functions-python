import logging
import os
import time
import pyodbc
import azure.functions as func
from .. import tools

# from ..tools import *

## import __app__.tools import *
## from __app__.tools import tools_math

def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    logging.info('Python HTTP trigger function processed a request.')

    num = req.params.get('number')
    if not num:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            num = req_body.get('number')

    if num:
        out = (float(num)+2)**2
        l1 = f"Linux function app 2 does magics with {num} and returns {out}! \n"
        dt1 = time.time()-start
        l1t = f"Time Elapsed(s) : {dt1} \n\n"

        # Call Common Functions
        sum1,_ = tools.sum1(num, 2)
        sub1,_ = tools.sub1(num, 2)
        pow1,_ = tools.pow1(num, 2)
        div1,_ = tools.div1(num, 2)
        l2 = f"Sum      : {sum1}! \n"
        l3 = f"Sub      : {sub1}! \n"
        l4 = f"Pow      : {pow1}! \n"
        l5 = f"Div      : {div1}! \n"

        # Test Azure SQL
        try:
            numprojs, connStr = test_sql()
        except:
            numprojs, connStr = "N/A", None
        l6 = f"# Projs  : {numprojs} \n"
        l7 = f"     by  : {connStr}  \n\n"


        dt2 = time.time()-start - dt1
        l8 = f"Time Elapsed on Common Funcs(s) : {dt2} \n"
        return func.HttpResponse(l1 + l1t + l2 + l3 + l4 + l5 + l6 + l7 + l8)
    else:
        dt1 = time.time()-start
        return func.HttpResponse(
             "Please pass a number to Linux Function App 2 on the query string or in the request body \n\n"  +
             f"Total Time Elapsed(s) : {dt1} \n",
             status_code=400
        )


def test_sql():
    # server = os.environ.get("sql_server")
    # port = os.environ.get("sql_port")
    # database =  os.environ.get("sql_database")
    # username =  os.environ.get("sql_username")
    # password =  os.environ.get("sql_password")
    # driver =  os.environ.get("sql_driver")
    # db = pyodbc.connect('DRIVER=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' %(driver, server, port, database, username, password))
    
    try:
        connStr = "SQLAZURECONNSTR_sqlConnectionString"
        db = pyodbc.connect( os.environ.get(connStr) )

    except Exception as e1:
        try:
            connStr = "dbConnectionString"
            db = pyodbc.connect( os.environ.get(connStr) )
        except Exception as e2:
            return "%s \n %s" %(str(e1),str(e2))
        



    # Execute SQL select statement
    cursor = db.cursor()
    cursor.execute("SELECT * FROM project")
    rows = cursor.fetchall()
    numprojs = len(rows)

    # Get the number of rows affected 
    # numrows = cursor.rowcount

    # Close the connection
    db.close()   
    return numprojs, connStr