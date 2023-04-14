from django.db import connection, reset_queries

import time
from functools import wraps


def check_query(func):
    """Decorator checks quality of db queries."""

    @wraps(func)
    def inner(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        print(f"Start count queries: {start_queries}")
        start = time.perf_counter()
        print(f"Start time: {start}")
        func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Finish time: {end}")
        end_queries = len(connection.queries)
        print(f"End count queries: {end_queries}")
        print(f'Queries quantity: {end_queries - start_queries}')
        print(f'Execution time: {end - start}')
    return inner
