from pydantic import BaseModel


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