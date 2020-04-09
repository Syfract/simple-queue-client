"""
Client for the simplest Message Queue server

It can be used to push to and pull from the simple queue server.
It can also be used as a template for the API.
"""
from typing import Union
from requests import get, post, HTTPError


class QueueDoesNotExists(Exception):
    """404 status code is received"""


class QueueServerIssue(Exception):
    """5xx status code is received"""


class QueueEmpty(Exception):
    """204 status code is received. Queue was empty!"""


class QueueClient:
    def __init__(self, host: str, port: int=None):
        if not host.startswith('http://'):
            host = 'http://' + host
        self.address = host if port is None else '%s:%d' % (host, port)

    def push(self, queue_name: str, element: Union[str, dict]):
        text = json = None
        if isinstance(element, str):
            text = element
        elif isinstance(element, dict):
            json = element

        res = post(self.address + '/push/' + queue_name, text, json)
        if res.status_code >= 500:
            raise QueueServerIssue()

    def pull(self, queue_name: str, raise_if_empty: bool = False):
        res = get(self.address + '/pull/' + queue_name)
        if res.status_code >= 500:
            raise QueueServerIssue()
        elif res.status_code == 404:
            raise QueueDoesNotExists()
        elif res.status_code == 204 and raise_if_empty:
            raise QueueEmpty()
        return res.text
