#!/usr/bin/env python3

import functools
import requests
import time

def retry_wrapper(_func=None, *, retry=5):
    def retry_logic_wrapper(func):
        @functools.wraps(func)
        def retry_logic(*args, **kargs):
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
            return rc
        return retry_logic

    if _func is None:
        return retry_logic_wrapper
    else:
        return retry_logic_wrapper(_func)
                
@retry_wrapper(retry=3)
def get_status_code(url):
    r = requests.get(url)
    return r.status_code

print(get_status_code('https://www.pinterest.com/god-damn-i-know-this-does-not-exist'))
print(get_status_code('https://www.pinterest.com'))
