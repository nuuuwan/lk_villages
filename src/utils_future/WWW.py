import requests
from utils import Log

TIMEOUT = 30

log = Log('WWW')


class WWW:
    def __init__(self, url):
        self.url = url

    def post(self, data=None):
        response = requests.post(self.url, data=data, timeout=TIMEOUT)
        content = response.text
        len(content) / 1_000_000
        # log.debug(f"POST {self.url} {data} ({n:.3f}MB) complete.")
        return content
