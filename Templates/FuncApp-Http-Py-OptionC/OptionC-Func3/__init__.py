import logging
import json
import time
import azure.functions as func
from .. import ToolsC as tools
# BREAKS
# from tools import subTC3, subTC4

def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Decode and return request body as JSON
        req_body = req.get_json()
    except ValueError:
        numA, numB = None, None
        pass
    else:
        numA = req_body.get('A')
        numB = req_body.get('B')        

    if numA and numB:
        # Call Common Functions
        sum1 = tools.sum1(numA, numB)
        sub2 = tools.sub2(numA, numB)

        # Only available if in ToolC
        # base level import is active "from .subTC3 import *"
        # pow3 = tools.pow3(numA, numB)
        # div4 = tools.div4(numA, numB)

        # Calling Sub Packages
        sub3_pow3 = tools.subTC3.sub3(numA, numB)
        sub4_div4 = tools.subTC4.sub4(numA, numB)


        dt1 = time.time()-start
        return func.HttpResponse(
            json.dumps({
                'method': req.method,
                'url': req.url,
                'headers': dict(req.headers),
                'params': dict(req.params),
                'get_body': req.get_body().decode(),
                'timer': dt1,
                'return': 'Function App recieved %s and %s' %({numA}, {numB}) ,
                'Sum': sum1,
                'Sub': sub2,
                'Pow': sub3_pow3,
                'Div': sub4_div4
            })
            )

    else:
        dt1 = time.time()-start
        return func.HttpResponse(
            json.dumps({
                'method': req.method,
                'url': req.url,
                'headers': dict(req.headers),
                'params': dict(req.params),
                'get_body': req.get_body().decode(),
                'timer': dt1,
                'return': 'Please pass numbers A,B to Function App in the request body'
            })
            , status_code=400
        )