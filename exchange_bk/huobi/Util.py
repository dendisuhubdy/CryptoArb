#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import json

import urllib
from datetime import datetime
import requests
import urllib2
import urlparse
from util.util import *
#from util import *

# timeout in 5 seconds:
TIMEOUT = 5

# API_HOST = 'be.huobi.com'
API_HOST = "api.huobipro.com"

SCHEME = 'https'

# language setting: 'zh-CN', 'en':
LANG = 'zh-CN'

DEFAULT_GET_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': LANG,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

DEFAULT_POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': LANG,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

# API 请求地址
#MARKET_URL = TRADE_URL = "https://be.huobi.com"
MARKET_URL = TRADE_URL = "https://api.huobipro.com"


def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    params.pop("account", None)
    postdata = urllib.urlencode(params)
    try:
        response = requests.get(url, postdata, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail", "msg":"get acoount fail"}
    except Exception as e:
        print "httpGet failed, detail is:%s" % e
        return {"status": "fail", "msg": e}


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "User-Agent": "Chrome/39.0.2171.71",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    try:
        response = requests.post(url, postdata, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print "httpPost failed, detail is:%s" % e
        return


def api_key_get(params, request_path):
    method = 'GET'
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    ACCESS_KEY, SECRET_KEY = get_account_key("huobi", params.pop("account", None))
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_name = host_url = TRADE_URL
    host_name = urlparse.urlparse(host_url).hostname
    host_name = host_name.lower()

    params['Signature'] = createSign(
        params, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    ACCESS_KEY, SECRET_KEY = get_account_key("huobi", account=params.pop("account", None))
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = TRADE_URL
    host_name = urlparse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params['Signature'] = createSign(
        params, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.urlencode(params)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
