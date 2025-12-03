import csv
import json

import asyncpg
from configurations.postgress_config import PostgresConfig
from configurations.raw_data_config import RawDataConfig
from models.prospect import Prospect
from services.inspector_service import InspectorService


class InspectorInitiator:
    def __init__(self) -> None:
        """
        Construct the InspectorInitiator and initialize configuration objects.

        Attributes initialized:
            raw_data_config:
                Instance of RawDataConfig, responsible for reading and
                validating raw input files used in the inspection process.

            postgres_config:
                Instance of PostgresConfig, containing all configuration
                required to connect to the PostgresSQL database.
        """
        self._raw_data_config = RawDataConfig()
        self._postgres_config = PostgresConfig()

    def initiate(self) -> InspectorService:
        """Initiate selector service."""
        # Loads prospects
        with open(self._raw_data_config.prospects_path, encoding="utf-8") as f:
            json_prospects = list(csv.DictReader(f))
        prospects = [Prospect(**prospect) for prospect in json_prospects]

        # Load users locations settings
        with open(self._raw_data_config.user_locations_settings_path, encoding="utf-8") as f:
            users_locations_settings = json.loads(f.read())

        # Load country region mapping
        with open(self._raw_data_config.country_to_region_mapping_path, encoding="utf-8") as f:
            country_region_mapping = json.loads(f.read())

        return InspectorService(
            prospects=prospects,
            users_locations_settings=users_locations_settings,
            country_to_region=country_region_mapping,
            postgres_accessor=asyncpg.create_pool(self._postgres_config.postgres_dsn),
        )
