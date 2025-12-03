from collections import defaultdict

from accessors.postgres_accessor import PostgresAccessor
from models.prospect import Prospect
from models.user_location_settings import UserLocationSettings


class InspectorService:
    def __init__(self,
                 postgres_accessor: PostgresAccessor,
                 country_to_region: dict[str, list[str]],
                 users_locations_settings: dict[str, dict[str, list[str]]],
                 prospects: list[Prospect]) -> None:
        self._postgres_accessor = postgres_accessor
        self._users_locations_settings = users_locations_settings
        self._country_to_region = country_to_region
        self._prospects = prospects

    async def update_selected_prospects(self) -> Prospect:
        """update selected prospects via postgres accessor"""
        pass

    @staticmethod
    def _check_prospect_locations(user_settings: UserLocationSettings, prospect_locations: list[str]) -> bool:
        """Check if prospect locations included in user locations settings"""
        if not set(prospect_locations).isdisjoint(user_settings.location_include) and set(
                prospect_locations).isdisjoint(user_settings.location_exclude):
            return True
        return False

    def _validate_region(self, user_settings: UserLocationSettings, prospect_locations: list[str]) -> bool:
        """Validate prospect region"""
        for location in prospect_locations:
            if self._country_to_region.get(location, None):
                if self._check_prospect_locations(user_settings, self._country_to_region[location]):
                    return True
        return False

    def inspect_users_prospects(self) -> dict[str, dict[str, bool]]:
        """Select prospects based on user location settings."""
        relevant_prospects_to_user: dict[str, dict[str, bool]] = defaultdict(dict)

        # Caches user settings if user is already read.
        settings_cache: dict[str, UserLocationSettings] = {}
        for prospect in self._prospects:
            user_id = prospect.user_id
            raw_settings = self._users_locations_settings.get(user_id)
            if not raw_settings:
                continue

            if user_id not in settings_cache:
                UserLocationSettings(**raw_settings)
                settings_cache[user_id] = UserLocationSettings(**raw_settings)

            user_settings = settings_cache[user_id]
            prospect_locations = [prospect.company_country, prospect.company_state]
            is_relevant = (
                    self._check_prospect_locations(user_settings, prospect_locations)
                    or self._validate_region(user_settings, prospect_locations)
            )
            relevant_prospects_to_user[user_id][prospect.prospect_id] = is_relevant

        return dict(relevant_prospects_to_user)
