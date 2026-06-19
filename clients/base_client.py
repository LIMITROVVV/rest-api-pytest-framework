import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, session: requests.Session, base_url: str):
        self._session = session
        self._base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def _log(self, method: str, url: str, response: requests.Response) -> None:
        logger.debug("%s %s -> %d", method.upper(), url, response.status_code)

    def get(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        resp = self._session.get(url, **kwargs)
        self._log("GET", url, resp)
        return resp

    def post(self, path: str, json: Any = None, **kwargs) -> requests.Response:
        url = self._url(path)
        resp = self._session.post(url, json=json, **kwargs)
        self._log("POST", url, resp)
        return resp

    def put(self, path: str, json: Any = None, **kwargs) -> requests.Response:
        url = self._url(path)
        resp = self._session.put(url, json=json, **kwargs)
        self._log("PUT", url, resp)
        return resp

    def patch(self, path: str, json: Any = None, **kwargs) -> requests.Response:
        url = self._url(path)
        resp = self._session.patch(url, json=json, **kwargs)
        self._log("PATCH", url, resp)
        return resp

    def delete(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        resp = self._session.delete(url, **kwargs)
        self._log("DELETE", url, resp)
        return resp
