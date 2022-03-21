#!/usr/bin/env python3

import functools
import requests
import time

def retry_wrapper(func):
    @functools.wraps(func)
    def retry_logic(*args, **kargs):
        retry = 5
        gap = 0
        n = 0

        while True:
            if n == retry:
                print("exhausted. exited.")
                break
            rc = func(*args, **kargs)
            if rc != 200:
                n += 1
                sleep_time = 2 ** gap
                gap += 1
                print("sleep %d seconds for the %d retry - rc: %d" %(sleep_time, n, rc))
                time.sleep(sleep_time)
            else:
                print("status_code: %d" %(rc))
                break
        return func(*args, **kargs)
    return retry_logic
                
@retry_wrapper
def get_status_code(url):
    r = requests.get(url)
    return r.status_code

get_status_code('https://www.pinterest.com/god-damn-i-know-this-does-not-exist')
