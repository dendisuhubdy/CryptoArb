# !/usr/bin/env python
# coding:utf-8

import functools
import threading
import time
from datetime import datetime
from ConfigParser import ConfigParser
import os



def get_base_spreads(price, base= 0.001):
    price = float(price)
    #return abs(price * base)
    return price * base


def get_account_key(exchange, account=None):
    if not account:
        return None, None
    cf = ConfigParser()
    cf.read('../config/%s.ini' % account)
    apikey = cf.get('%s' % exchange, 'api_key')
    secretkey = cf.get('%s' % exchange, 'secret_key')
    return apikey, secretkey


def get_exchange_coin_address(exchange, coin, account=None):
    if not account:
        return None, None,None
    cf = ConfigParser()
    cf.read('../config/%s.ini' % account)
    address = cf.get('%s' % exchange,  coin + "_address")
    fee = cf.getfloat('%s' % exchange, coin + "_fee")
    tag = cf.get('%s' % exchange,  coin + "_tag")
    return address, fee, tag

def get_tradepwd(exchange, account=None):
    if not account:
        return None
    cf = ConfigParser()
    cf.read('../config/%s.ini' % account)
    tradepwd = cf.get('%s' % exchange, 'tradepwd')
    return tradepwd


def async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        my_thread.setDaemon(True)
        my_thread.start()
    return wrapper

@async
def Log(owner, coinType, msg):
    now_md = time.strftime("%Y%m%d")
    if not os.path.isdir("log"):
        os.mkdir("log")
    with open('log/%s_%s_%s.log' % (owner,coinType, now_md), 'a') as t:
        now = datetime.now()
        str_time = now.strftime('%Y-%m-%d %H:%M:%S')
        msg = "[" + str_time + "]" + ' ' + msg
        t.write(msg)

@async
def dblog(coinType, msg):
    pass

@async
def alert(coinType, msg):
    pass

@async
def wxbot(coinType, msg):
    pass
