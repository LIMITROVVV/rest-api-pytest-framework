import json
import os

import allure
import jsonschema
import pytest

from clients.users_client import UsersClient

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")


def load_schema(name: str) -> dict:
    with open(os.path.join(SCHEMAS_DIR, name)) as f:
        return json.load(f)


@pytest.fixture
def users(http_session, base_url):
    return UsersClient(http_session, base_url)


@allure.suite("Users")
class TestUsers:

    @allure.title("list users - page 1 returns expected shape")
    @pytest.mark.smoke
    @pytest.mark.users
    def test_list_users_page1(self, users):
        resp = users.list_users(page=1)

        assert resp.status_code == 200
        body = resp.json()
        assert body["page"] == 1
        assert len(body["data"]) > 0

    @allure.title("list users - page 2 returns different data")
    @pytest.mark.users
    def test_list_users_page2(self, users):
        page1 = users.list_users(page=1).json()["data"]
        page2 = users.list_users(page=2).json()["data"]

        ids_p1 = {u["id"] for u in page1}
        ids_p2 = {u["id"] for u in page2}
        assert ids_p1.isdisjoint(ids_p2), "pages should not share user ids"

    @allure.title("get single user by id")
    @pytest.mark.smoke
    @pytest.mark.users
    def test_get_user(self, users):
        resp = users.get_user(2)

        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["id"] == 2
        assert "@" in data["email"]

    @allure.title("get user - 404 for non-existent id")
    @pytest.mark.users
    def test_get_user_not_found(self, users):
        resp = users.get_user(9999)

        assert resp.status_code == 404
        # reqres returns empty body on 404
        assert resp.json() == {}

    @allure.title("create user returns 201 with name and job")
    @pytest.mark.smoke
    @pytest.mark.users
    def test_create_user(self, users):
        resp = users.create_user(name="morpheus", job="leader")

        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == "morpheus"
        assert body["job"] == "leader"
        assert "id" in body
        assert "createdAt" in body

    @allure.title("user response matches json schema")
    @pytest.mark.regression
    @pytest.mark.users
    def test_get_user_schema(self, users):
        resp = users.get_user(1)
        schema = load_schema("user.json")

        assert resp.status_code == 200
        user_data = resp.json()["data"]

        # raises jsonschema.ValidationError if schema doesn't match
        jsonschema.validate(instance=user_data, schema=schema)

    @allure.title("update user - put returns 200 with updated fields")
    @pytest.mark.users
    def test_update_user(self, users):
        resp = users.update_user(user_id=2, name="morpheus", job="zion resident")

        assert resp.status_code == 200
        body = resp.json()
        assert body["job"] == "zion resident"
        assert "updatedAt" in body

    @allure.title("delete user returns 204")
    @pytest.mark.users
    def test_delete_user(self, users):
        resp = users.delete_user(user_id=2)

        assert resp.status_code == 204
        assert resp.text == ""
