import pytest
import json

from unittest.mock import patch, Mock

from src.main import Gender, get_highest_hero


with open("./tests/data/highest_woman_with_job.json") as data:
    highest_woman_with_job = json.load(data)

with open("./tests/data/highest_woman_without_job.json") as data:
    highest_woman_without_job = json.load(data)

with open("./tests/data/highest_man_with_job.json") as data:
    highest_man_with_job = json.load(data)

with open("./tests/data/highest_man_without_job.json") as data:
    highest_man_without_job = json.load(data)


@patch('src.main.requests.get')
@pytest.mark.parametrize(
        "gender, have_job, hero",
        [
            (Gender.female, True, highest_woman_with_job),
            (Gender.female, False, highest_woman_without_job),
            (Gender.male, True, highest_man_with_job),
            (Gender.male, False, highest_man_without_job)
        ]
)
def test_find_highest_hero(mock_get: Mock, gender, have_job, hero):
    mock_get.return_value.status_code = 200

    with open('./tests/data/heros.json') as json_data:
        data = json.load(json_data)

    mock_get.return_value.json.return_value = data

    assert get_highest_hero(gender, have_job) == hero


def test_invalid_gender():
    with pytest.raises(TypeError):
        get_highest_hero('non-binary', True)


@patch('src.main.requests.get')
def test_highest_hero_not_found(mock_get: Mock):
    mock_get.return_value.status_code = 200

    with open('./tests/data/valid_heros.json') as json_data:
        data = json.load(json_data)

    mock_get.return_value.json.return_value = data

    assert get_highest_hero(Gender.female, True) is None
