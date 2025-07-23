from pydantic import BaseModel, field_validator
from typing import Optional, List


class Appearance(BaseModel):
    """Represents appearance information about hero
       from API with fields from it
    """

    eyeColor: Optional[str]
    gender: Optional[str]
    hairColor: Optional[str]
    height: List[str]  # cm
    race: Optional[str]
    weight: Optional[List[str]]

    @property
    def converted_height(self):
        height_SI = self.height[1]
        height_value, height_measurement = height_SI.split()

        if height_measurement == 'meters':
            return int(float(height_value) * 100)
        elif height_measurement == 'cm':
            return int(height_value)

    @field_validator('height', mode='before')
    @classmethod
    def validate_height(cls, height: List[str]):
        try:
            height_SI = height[1]
        except IndexError:
            raise ValueError(
                "Invalid height. Must be string list with lenght 2"
            )

        height_value, height_measurement = height_SI.split()

        if (
            height_measurement != 'meters' and height_measurement != 'cm'
            or float(height_value) <= 0
        ):
            raise ValueError("Invalid height measurement")

        return height


class Biography(BaseModel):
    """Represents biography information about hero from API with fields from it
    """

    aliases: Optional[List[str]]
    alignment: Optional[str]
    alterEgos: Optional[str]
    firstAppearance: Optional[str]
    fullName: Optional[str]
    placeOfBirth: Optional[str]
    publisher: Optional[str]


class Connections(BaseModel):
    """Represents connections information about hero
       from API with fields from it
    """

    groupAffiliation: Optional[str]
    relatives: Optional[str]


class Images(BaseModel):
    """Represents hero images information from API with fields from it
    """

    lg: Optional[str]
    md: Optional[str]
    sm: Optional[str]
    xs: Optional[str]


class Powerstats(BaseModel):
    """Represents hero powerstats from API with fields from it
    """

    combat: Optional[int]
    durability: Optional[int]
    intelligence: Optional[int]
    power: Optional[int]
    speed: Optional[int]
    strength: Optional[int]


class Work(BaseModel):
    """Represents information about hero's job from API with fields from it
    """

    base: Optional[str]
    occupation: Optional[str]


class Hero(BaseModel):
    """Represents hero from API with fields from it
    """

    id: int
    name: Optional[str]
    slug: Optional[str]
    appearance: Appearance
    biography: Biography
    connections: Connections
    images: Images
    powerstats: Powerstats
    work: Work
