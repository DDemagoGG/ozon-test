import pytest
import json

from requests.exceptions import RequestException
from unittest.mock import patch, Mock

from src.main import get_API_heros


@patch('src.main.requests.get')
def test_wrong_API_status_code(mock_get: Mock):
    mock_get.return_value.status_code = 500

    with pytest.raises(RequestException):
        get_API_heros()


@patch('src.main.requests.get')
def test_empty_response(mock_get: Mock):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    assert get_API_heros() == []


@patch('src.main.requests.get')
def test_invalid_heros(mock_get: Mock):
    mock_get.return_value.status_code = 200

    with open('./tests/data/invalid_heros.json') as json_data:
        data = json.load(json_data)
    mock_get.return_value.json.return_value = data

    assert get_API_heros() == []


@patch('src.main.requests.get')
def test_all_valid_heros(mock_get: Mock):
    mock_get.return_value.status_code = 200

    with open('./tests/data/valid_heros.json') as json_data:
        data = json.load(json_data)
    mock_get.return_value.json.return_value = data
    heros = get_API_heros()

    assert len(heros) == len(data)


@patch('src.main.requests.get')
def test_valid_with_invalid_heros(mock_get: Mock):
    mock_get.return_value.status_code = 200

    with open('./tests/data/valid_heros.json') as json_data:
        data1 = json.load(json_data)

    with open('./tests/data/invalid_heros.json') as json_data:
        data2 = json.load(json_data)

    mock_get.return_value.json.return_value = data1 + data2
    heros = get_API_heros()

    assert len(heros) == len(data1)
