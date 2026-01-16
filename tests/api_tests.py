import pytest
from unittest.mock import AsyncMock, ANY
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_depends import get_db


client =TestClient(app)


@pytest.fixture
def override_get_db():
    async def fake_db():
        yield AsyncMock()  # фейковая сессия SQLAlchemy
    return fake_db


@pytest.fixture
def client_with_overrides(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}  # сбросить после теста


FAKE_BTC_RESULT = {"answer": [{
                                "date_time": "2026-01-14T15:34:06.181281",
                                "rate": 96802.37
                              },
                              {
                                "date_time": "2026-01-14T15:35:00.141412",
                                "rate": 96872.72
                              },
                              {
                                "date_time": "2026-01-14T15:36:00.148502",
                                "rate": 96857.23
                              }]
                    }


FAKE_ETH_RESULT = {"answer": [{
                                "rate": 3351.66,
                                "date_time": "2026-01-14T15:34:06.181220"
                              },
                              {
                                "rate": 3355.42,
                                "date_time": "2026-01-14T15:35:00.141703"
                              },
                              {
                                "rate": 3353.42,
                                "date_time": "2026-01-14T15:36:00.137134"
                              }]
                    }


CURRENCY_TEST_CASES = [
    ('btc', FAKE_BTC_RESULT),
    ('eth', FAKE_ETH_RESULT),
]

### Ендпоинт для всех записей в базе ###
@pytest.mark.asyncio # Проверяем работу при корректных данных, когда на входе eth или btc
@pytest.mark.parametrize("currency, mock_result", CURRENCY_TEST_CASES)
async def test_get_all_current_rates_for_currencies(
        currency, mock_result,
        client_with_overrides, monkeypatch
):
    mock_db_call = AsyncMock(return_value=mock_result)
    monkeypatch.setattr(
        "app.routers.rates.get_all_current_rates_form_db",
        mock_db_call
    )

    response = client_with_overrides.get(
        "/rates/all_current_rates",
        params={"currency": currency}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == mock_result

    mock_db_call.assert_awaited_once_with(ANY, currency)


@pytest.mark.asyncio # Проверяем работу при некорректных данных
@pytest.mark.parametrize("currency, expected_status", [('invalid', 422)])
async def test_get_all_current_rates_with_invalid(currency, expected_status, client_with_overrides):
    response = client_with_overrides.get("/rates/all_current_rates", params={'currency': currency})
    assert response.status_code == expected_status


### Эендпоинт с временным интервалом ###
@pytest.mark.asyncio # Проверяем работу при корректных данных, когда на входе eth или btc
@pytest.mark.parametrize("currency, mock_result", CURRENCY_TEST_CASES)
async def test_get_interval_rates_with_data(
        currency, mock_result,
        client_with_overrides, monkeypatch
):
    mock_db_call = AsyncMock(return_value=mock_result)
    monkeypatch.setattr(
        "app.routers.rates.get_interval_rates_form_db",
        mock_db_call
    )

    response = client_with_overrides.get(
        "/rates/interval_rates",
        params={"currency": currency}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == mock_result

    mock_db_call.assert_awaited_once_with(ANY, currency, ANY)


@pytest.mark.asyncio # Случай, когда в интервале нет данных
@pytest.mark.parametrize("currency", [('btc'), ('eth')])
async def test_get_interval_rates_no_data(
        currency,
        client_with_overrides, monkeypatch
):
    mock_db_call = AsyncMock(return_value=[])
    monkeypatch.setattr(
        "app.routers.rates.get_interval_rates_form_db",
        mock_db_call
    )

    response = client_with_overrides.get(
        "/rates/interval_rates",
        params={"currency": currency}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == 'No data found'

    mock_db_call.assert_awaited_once_with(ANY, currency, ANY)


@pytest.mark.asyncio # Случай, когда не корректные данные
@pytest.mark.parametrize("currency, expected_status", [('invalid', 422)])
async def test_get_interval_rates_with_invalid(currency, expected_status, client_with_overrides):
    response = client_with_overrides.get("/rates/interval_rates", params={'currency': currency})
    assert response.status_code == expected_status


@pytest.mark.asyncio # Играемся с временными интервалами
@pytest.mark.parametrize("start_date, end_date, expected_status", [
    ('2026-01-14T15:00:00', '2026-01-14T14:00:00', 422),  # start_date > end_date
    ('2026-01-14T15:00:00', '2026-01-14T15:00:00', 422),  # start_date == end_date
])
async def test_get_interval_rates_invalid_dates(start_date, end_date, expected_status, client_with_overrides):
    response = client_with_overrides.get(
        "/rates/interval_rates",
        params={
            'currency': 'btc',
            'start_date': start_date,
            'end_date': end_date
        }
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_get_interval_rates_valid_dates(client_with_overrides, monkeypatch):
    mock_db_call = AsyncMock(return_value=FAKE_BTC_RESULT)
    monkeypatch.setattr(
        "app.routers.rates.get_interval_rates_form_db",
        mock_db_call
    )

    response = client_with_overrides.get(
        "/rates/interval_rates",
        params={
            'currency': 'btc',
            'start_date': '2026-01-14T14:00:00',
            'end_date': '2026-01-14T16:00:00'
        }
    )

    assert response.status_code == 200
    assert response.json()["answer"] == FAKE_BTC_RESULT

    mock_db_call.assert_awaited_once_with(ANY, 'btc', ANY)


FAKE_BTC_RESULT = {"answer": [{
                                "date_time": "2026-01-14T15:34:06.181281",
                                "rate": 96802.37
                              }]
                    }


FAKE_ETH_RESULT = {"answer": [{
                                "rate": 3351.66,
                                "date_time": "2026-01-14T15:34:06.181220"
                              }]
                    }


CURRENCY_TEST_CASES = [
    ('btc', FAKE_BTC_RESULT),
    ('eth', FAKE_ETH_RESULT),
]


### Эндпоинт, который присылает самую свежую запись ###
@pytest.mark.asyncio
@pytest.mark.parametrize("currency, mock_result", CURRENCY_TEST_CASES)
async def test_get_last_current_rates_for_currencies(
        currency, mock_result,
        client_with_overrides, monkeypatch
):
    mock_db_call = AsyncMock(return_value=mock_result)
    monkeypatch.setattr(
        "app.routers.rates.get_last_current_rates_form_db",
        mock_db_call
    )

    response = client_with_overrides.get(
        "/rates/last_current_rates",
        params={"currency": currency}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == mock_result

    mock_db_call.assert_awaited_once_with(ANY, currency)


@pytest.mark.asyncio
@pytest.mark.parametrize("currency, expected_status", [('invalid', 422)])
async def test_get_last_current_rates_with_invalid(currency, expected_status, client_with_overrides):
    response = client_with_overrides.get("/rates/last_current_rates", params={'currency': currency})
    assert response.status_code == expected_status

# python -m pytest tests/api_tests.py