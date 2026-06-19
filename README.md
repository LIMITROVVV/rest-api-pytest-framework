# rest-api-pytest-framework

Test automation framework for REST APIs. I use this as a baseline when starting a new project - clone, swap the base URL and clients, done.

Ran against [reqres.in](https://reqres.in) as a demo target since it's public, stable, and has realistic CRUD + auth endpoints.

## stack

- pytest + requests
- jsonschema for response validation
- allure for reports
- python-dotenv for local env config
- GitHub Actions for CI

## structure

```
clients/          service-object layer (one file per API resource)
schemas/          json schemas for response validation
tests/            test files, roughly mirroring clients/
conftest.py       shared fixtures
```

## running locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# optional, defaults are in conftest
cp .env.example .env

pytest tests/ -v
```

With allure report:

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

Run a specific marker:

```bash
pytest -m smoke
pytest -m "not slow"
```

## env vars

| var | default | notes |
|-----|---------|-------|
| `BASE_URL` | `https://reqres.in` | swap to your target |
| `API_KEY` | `reqres-free-v1` | reqres free tier key |

## notes

- reqres.in returns fake data but validates inputs - good enough for contract testing patterns
- schemas/ only covers the happy path shapes, edge case validation is done inline
- TODO: add response time assertions to smoke suite
