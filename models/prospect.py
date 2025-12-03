from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

class ProspectMatch(StrEnum):
    DISTRICT = 'DISTRICT'
    REGION = 'REGION'
    NONE = 'NONE'

class Prospect(BaseModel):
    """
    User Prospect

    Attributes:
        user_id: The user id.
        prospect_id: The prospect id to check.
        company_country: The company country to check.
        company_state: The company state to check.
    """
    user_id: str
    prospect_id: str
    company_country: str
    company_state: str

class InspectedProspect(BaseModel):
    """
    Inspected Prospect

    Attributes:
        user_id: The user id.
        prospect_id: The prospect id to check.
        qualifies: Whether the prospect is qualified or not.
        matched_with: list of location match with the prospect.
        matched_by: list of prospect matches types.
        evaluated_at: evaluated at of the prospect.
    """
    user_id: str
    prospect_id: str
    qualifies: bool
    matched_with: Optional[list[str]] = None
    matched_by: Optional[list[ProspectMatch]] = None
    evaluated_at: datetime
