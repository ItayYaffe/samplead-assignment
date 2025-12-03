from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator


def none_to_list(v) -> None:
    """Ensure that none value is a list."""
    return [] if v is None else v

class UserLocationSettings(BaseModel):
    """
    Represents user location settings.

    Attributes:
        location_include: A list of locations the user is interested in.
        location_exclude: A list of locations the user is not interested in.
    """
    location_include: Annotated[list[str], BeforeValidator(none_to_list)] = Field(default_factory=list)
    location_exclude: Annotated[list[str], BeforeValidator(none_to_list)] = Field(default_factory=list)
