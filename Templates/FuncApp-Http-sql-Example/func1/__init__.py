import logging
import os
import time
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    logging.info('Python HTTP trigger function processed a request.')

    # Decode 'Name', HTTP Get (URL) Params
    name = req.params.get('name')
    if not name:
        try:
            # Decode and return request body as JSON
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        envVal1 = os.environ.get("FUNCTIONS_WORKER_RUNTIME")
        envVal2 = os.environ.get("dbConnectionValue")
        connStr1 = os.environ.get("SQLAZURECONNSTR_sqlConnectionString")
        connStr2 = os.environ.get("SQLCONNSTR_sqlConnectionString")
        if isinstance(envVal2,str):
            envVal2 = envVal2[0:23]
        if isinstance(connStr1,str):
            connStr1 = connStr1[0:23]
        if isinstance(connStr2,str):
            connStr2 = connStr2[0:23] 

        l1 = f"Hello {name} from Linux function app 1! \n\n"
        l2 = f"Environment Variables \n"
        l3 = f"WORKER           : {envVal1}    \n"
        l4 = f"DB       Values  : {envVal2} ...\n\n"        
        l5 = f"Environment Connection Strings \n"
        l6 = f"SQLAZURE CONNSTR : {connStr1} ...\n"
        l7 = f"SQL      CONNSTR : {connStr2} ...\n\n"
        dt = time.time()-start
        l8 = f"Total Time Elapsed(s) : {dt} \n"
        return func.HttpResponse(l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8)
    else:
        dt = time.time()-start
        return func.HttpResponse(
             "Please pass a name to Linux Function App 1 on the query string or in the request body \n\n" +
             f"Total Time Elapsed(s) : {dt} \n",
             status_code=400
        )
