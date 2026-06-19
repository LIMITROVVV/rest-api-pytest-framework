import os
import allure
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://reqres.in")


@pytest.fixture(scope="session")
def api_key():
    return os.getenv("API_KEY", "reqres-free-v1")


@pytest.fixture(scope="session")
def http_session(api_key):
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    })
    yield session
    session.close()


# attach request/response to allure on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        response = getattr(item, "_last_response", None)
        if response is not None:
            allure.attach(
                body=f"{response.request.method} {response.url}\n"
                     f"Status: {response.status_code}\n\n"
                     f"{response.text}",
                name="response",
                attachment_type=allure.attachment_type.TEXT,
            )
