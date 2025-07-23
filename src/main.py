import requests

from enum import Enum
from typing import List
from pydantic import ValidationError

from models import Hero


BASE_URL = "https://akabab.github.io/superhero-api/api"


class Gender(str, Enum):
    """Represents the gender of the hero
    """

    male = "Male"
    female = "Female"


def get_API_heros() -> List[Hero]:
    """Get all hero information from API with validation
    """

    response = requests.get(BASE_URL + "/all.json")
    if response.status_code != 200:
        raise requests.exceptions.RequestException(response=response)

    valid_heros = []

    for hero in response.json():
        try:
            valid_hero = Hero(**hero)
        except ValidationError:
            continue

        valid_heros.append(valid_hero)

    return valid_heros


def get_highest_hero(gender: Gender, have_job: bool) -> dict:
    """Get the highest hero by gender and job existence

    :param gender: instance of :class:`Gender` class
    :param have_job: indicates whether the hero has a job
    :return: json with hero information from API
    :rtype: dict
    :raises requests.exceptions.RequestException: if API doesn't respond
    """

    if not isinstance(gender, Gender):
        raise TypeError("Invalid gender")

    data = get_API_heros()
    max_height = -1
    highest_hero_original_index = -1
    cur_hero_index = -1

    for hero in data:

        cur_hero_index += 1

        hero_have_job = hero.work.occupation is not None \
            and hero.work.occupation != '-'
        hero_gender = hero.appearance.gender
        hero_height = hero.appearance.converted_height

        if hero_gender == gender.value and hero_have_job == have_job:
            if max_height < hero_height:
                highest_hero_original_index = cur_hero_index
                max_height = hero_height

    if max_height == -1:
        return None

    return data[highest_hero_original_index].model_dump()
