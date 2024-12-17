import logging
import time
from functools import wraps

logger = logging.getLogger('orix-poc-logger')

def log_execution_time_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f'''\n\t===>\tFunction '{func.__name__}' executed in {
              execution_time:.4f} seconds\n''')
        return result
    return wrapper

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f'''Function '{func.__name__}' executed in {
              execution_time:.4f} seconds\n''')
        return result
    return wrapper
