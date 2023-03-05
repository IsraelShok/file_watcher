import time
from functools import wraps


def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 5
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except:
                if i == max_retries - 1:
                    raise
                else:
                    time.sleep(2)
                    continue
    return wrapper
