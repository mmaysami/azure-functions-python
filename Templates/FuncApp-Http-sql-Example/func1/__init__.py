import logging
import os
import time
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        val1 = os.environ.get("FUNCTIONS_WORKER_RUNTIME")
        val2 = os.environ.get("dbConnectionString")
        sql1 = os.environ.get("SQLAZURECONNSTR_sqlConnectionString")
        sql2 = os.environ.get("SQLCONNSTR_sqlConnectionString")
        if isinstance(val2,str):
            val2 = val2[0:10]
        if isinstance(sql1,str):
            sql1 = sql1[0:10]
        if isinstance(sql2,str):
            sql2 = sql2[0:10] 

        l1 = f"Hello {name} from Linux function app 1! \n\n"
        l2 = f"WORKER           : {val1}    \n"
        l3 = f"DB       CONNSTR : {val2} ...\n"        
        l4 = f"SQLAZURE CONNSTR : {sql1} ...\n"
        l5 = f"SQL      CONNSTR : {sql2} ...\n\n"
        dt = time.time()-start
        l6 = f"Total Time Elapsed(s) : {dt} \n"
        return func.HttpResponse(l1 + l2 + l3 + l4 + l5 + l6)
    else:
        dt = time.time()-start
        return func.HttpResponse(
             "Please pass a name to Linux Function App 1 on the query string or in the request body \n\n" +
             f"Total Time Elapsed(s) : {dt} \n",
             status_code=400
        )
