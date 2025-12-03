import csv
from datetime import datetime
from collections import defaultdict
from itertools import chain

import asyncpg

from configurations.postgress_config import POSTGRES_INSERT_QUERY
from models.prospect import Prospect, ProspectMatch, InspectedProspect
from models.user_location_settings import UserLocationSettings


class InspectorService:
    def __init__(self,
                 postgres_accessor: asyncpg.Pool,
                 country_to_region: dict[str, list[str]],
                 users_locations_settings: dict[str, dict[str, list[str]]],
                 prospects: list[Prospect]) -> None:
        """Initialize the service with database access and input data.

        Args:
            postgres_accessor:
                A connection pool (asyncpg.Pool) used for executing INSERT
                operations into PostgresSQL.

            country_to_region:
                Country-to-region mapping. Keys are country codes,
                values are lists of regions that contain that country.

            users_locations_settings:
                Raw location settings per user. Each key is a user_id, and the
                value is a dict that can be unpacked into UserLocationSettings.

            prospects:
                A list of Prospect objects representing the prospects that
                should be inspected for qualification.
        """
        self._postgres_accessor = postgres_accessor
        self._users_locations_settings = users_locations_settings
        self._country_to_region = country_to_region
        self._prospects = prospects

    async def insert_inspected_prospects_to_postgres(self, prospects: list[InspectedProspect]) -> None:
        """update selected prospects via postgres accessor"""
        records = [
            (
                prospect.user_id,
                prospect.prospect_id,
                prospect.qualifies,
                prospect.matched_with or [],
                [m.value for m in (prospect.matched_by or [])],
                prospect.evaluated_at,
            )
            for prospect in prospects
        ]
        async with self._postgres_accessor.acquire() as conn:
            await conn.executemany(POSTGRES_INSERT_QUERY, records)
    @staticmethod
    def export_inspected_prospects_to_csv(prospects: list[InspectedProspect]) -> None:
        """Export a list of InspectedProspect objects into a CSV file."""

        fieldnames = list(InspectedProspect.model_fields.keys())

        with open('./inspected_prospects.csv', "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in prospects:
                writer.writerow({
                    "user_id": item.user_id,
                    "prospect_id": item.prospect_id,
                    "qualifies": item.qualifies,
                    "matched_with": ",".join(item.matched_with or []),
                    "matched_by": ",".join([m.value for m in (item.matched_by or [])]),
                    "evaluated_at": item.evaluated_at.isoformat(),
                })

    def _check_prospect_locations(self, user_settings: UserLocationSettings,
                                  prospect_locations: list[str]) -> dict[ProspectMatch, set[str]] | None:
        """Check if prospect locations included in user locations settings"""
        matches = {}
        regions = []
        for location in prospect_locations:
            if self._country_to_region.get(location, None):
                regions.extend(self._country_to_region[location])

        if not set(prospect_locations).isdisjoint(user_settings.location_exclude):
            return None

        if not set(prospect_locations).isdisjoint(user_settings.location_include):
            matches[ProspectMatch.DISTRICT] = set(prospect_locations).intersection(user_settings.location_include)
        elif not set(regions).isdisjoint(user_settings.location_include):
            matches[ProspectMatch.REGION] = set(regions).intersection(user_settings.location_include)
        else:
            matches[ProspectMatch.NONE] = None
        return matches

    @staticmethod
    def _create_inspected_prospects(
            relevant_prospects_to_user: dict[str, dict[str, dict[ProspectMatch, set[str]]]]
    ) -> list[InspectedProspect]:
        """Create inspected prospect object"""
        inspected_prospects = []
        for user_id, prospect_status in relevant_prospects_to_user.items():
            for prospect_id, matches_dict in prospect_status.items():
                matched_by = list(matches_dict.keys())
                matched_with = list(matches_dict.values())
                inspected_prospects.append(
                    InspectedProspect(
                        user_id=user_id,
                        prospect_id=prospect_id,
                        qualifies=True if ProspectMatch.NONE not in matched_by else False,
                        matched_with=list(chain.from_iterable(matched_with)) if matched_with[0] else None,
                        matched_by=matched_by,
                        evaluated_at=datetime.now(),
                    )
                )
        return inspected_prospects

    def inspect_users_prospects(self) -> list[InspectedProspect]:
        """Select prospects based on user location settings."""
        relevant_prospects_to_user: dict[str, dict[str, dict[ProspectMatch, set[str]]]] = defaultdict(dict)

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
            matched_prospects = self._check_prospect_locations(user_settings, prospect_locations)
            if matched_prospects:
                relevant_prospects_to_user[user_id][prospect.prospect_id] = matched_prospects

        return self._create_inspected_prospects(relevant_prospects_to_user)
