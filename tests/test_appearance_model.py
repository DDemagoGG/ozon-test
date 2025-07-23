import pytest

from pydantic import ValidationError

from src.models import Appearance


@pytest.mark.parametrize(
    "hero_appearance, converted_height",
    [
        (
            {
                "eyeColor": "White",
                "gender": "Male",
                "hairColor": "No Hair",
                "height": ["1000", "304.8 meters"],
                "race": "Frost Giant",
                "weight": ["- lb", "0 kg"]
            },
            30480
        ),
        (
            {
                "eyeColor": "Brown",
                "gender": "Male",
                "hairColor": "White",
                "height": ["2'2", "66 cm"],
                "race": "Yoda's species",
                "weight": ["38 lb", "17 kg"]
            },
            66
        )
    ]
)
def test_convertion_and_validation_of_valid_hero(
    hero_appearance,
    converted_height
):
    try:
        validated_appearance = Appearance(**hero_appearance)
    except ValidationError:
        pytest.fail()

    assert validated_appearance.converted_height == converted_height


@pytest.mark.parametrize(
    "hero_height",
    [

        ["2'2", "66"],
        "66 cm",
        ["2'2", "66 m"],
        [],
        ["2'2", ""],
        ["2'2", "hello"],
        ["-", "0 cm"]
    ]
)
def test_invalid_hero_height_validation(hero_height):
    hero_appearance = {
        "eyeColor": "Brown",
        "gender": "Male",
        "hairColor": "White",
        "race": "Yoda's species",
        "weight": ["38 lb", "17 kg"]
    }
    hero_appearance['height'] = hero_height

    with pytest.raises(ValidationError):
        Appearance(**hero_appearance)


def test_no_height():
    hero_appearance = {
        "eyeColor": "Brown",
        "gender": "Male",
        "hairColor": "White",
        "race": "Yoda's species",
        "weight": ["38 lb", "17 kg"]
    }
    with pytest.raises(ValidationError):
        Appearance(**hero_appearance)
