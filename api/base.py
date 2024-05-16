from datetime import timedelta
from requests_cache import CachedSession, response
import requests

BASE_URL = "http://127.0.0.1:8000"
# session = CachedSession(
#     'cache/api_requests_cache',
#     expire_after=timedelta(minutes=25),
#     allowable_methods=['GET', 'POST', 'UPDATE', 'PATCH', 'DELETE'],
# )
session= requests