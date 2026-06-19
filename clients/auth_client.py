import requests
from .base_client import BaseClient


class AuthClient(BaseClient):
    def login(self, email: str, password: str) -> requests.Response:
        return self.post("/api/login", json={"email": email, "password": password})

    def register(self, email: str, password: str) -> requests.Response:
        return self.post("/api/register", json={"email": email, "password": password})
