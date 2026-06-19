import allure
import pytest

from clients.auth_client import AuthClient


@pytest.fixture
def auth(http_session, base_url):
    return AuthClient(http_session, base_url)


@allure.suite("Auth")
class TestAuth:

    @allure.title("login - valid credentials return token")
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_success(self, auth):
        resp = auth.login(email="eve.holt@reqres.in", password="cityslicka")

        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        assert len(body["token"]) > 0

    @allure.title("login - missing password returns 400")
    @pytest.mark.auth
    def test_login_missing_password(self, auth):
        resp = auth.login(email="eve.holt@reqres.in", password="")

        assert resp.status_code == 400
        assert "error" in resp.json()

    @allure.title("login - unknown user returns 400")
    @pytest.mark.auth
    def test_login_unknown_user(self, auth):
        resp = auth.login(email="nobody@nowhere.io", password="whatever")

        assert resp.status_code == 400

    @allure.title("register - valid payload returns id and token")
    @pytest.mark.auth
    def test_register_success(self, auth):
        resp = auth.register(email="eve.holt@reqres.in", password="pistol")

        assert resp.status_code == 200
        body = resp.json()
        assert "id" in body
        assert "token" in body

    @allure.title("register - missing password returns 400 with error message")
    @pytest.mark.auth
    def test_register_missing_password(self, auth):
        resp = auth.register(email="sydney@fife", password="")

        assert resp.status_code == 400
        error = resp.json().get("error", "")
        assert len(error) > 0
