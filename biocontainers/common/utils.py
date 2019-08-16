import requests
from ratelimit import limits, sleep_and_retry

ONE_MINUTE = 60


@sleep_and_retry
@limits(calls=1000, period=ONE_MINUTE)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response