import requests
from .base_client import BaseClient


class UsersClient(BaseClient):
    _base_path = "/api/users"

    def list_users(self, page: int = 1) -> requests.Response:
        return self.get(self._base_path, params={"page": page})

    def get_user(self, user_id: int) -> requests.Response:
        return self.get(f"{self._base_path}/{user_id}")

    def create_user(self, name: str, job: str) -> requests.Response:
        return self.post(self._base_path, json={"name": name, "job": job})

    def update_user(self, user_id: int, name: str, job: str) -> requests.Response:
        return self.put(f"{self._base_path}/{user_id}", json={"name": name, "job": job})

    def delete_user(self, user_id: int) -> requests.Response:
        return self.delete(f"{self._base_path}/{user_id}")
