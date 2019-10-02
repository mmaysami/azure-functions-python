import time

def sum2(a, b):
    a = float(a)
    b = float(b)
    return a+b


def sub2(a, b):
    a = float(a)
    b = float(b)
    return a-b


def pow2(a, b):
    start = time.time()
    a = float(a)
    b = float(b)
    return a**b


def div2(a, b):
    a = float(a)
    b = float(b)
    return a//b
