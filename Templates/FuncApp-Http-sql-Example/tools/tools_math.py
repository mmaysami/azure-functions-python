# import numpy as np
# import pandas as pd
# import sklearn
import time


def sum1(a, b):
    start = time.time()
    a = float(a)
    b = float(b)
    return a+b, time.time()-start


def sub1(a, b):
    start = time.time()
    a = float(a)
    b = float(b)
    return a-b, time.time()-start


def pow1(a, b):
    start = time.time()
    a = float(a)
    b = float(b)
    return a**b, time.time()-start


def div1(a, b):
    start = time.time()
    a = float(a)
    b = float(b)
    return a//b, time.time()-start

