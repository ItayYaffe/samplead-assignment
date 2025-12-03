from pydantic_settings import BaseSettings


class RawDataConfig(BaseSettings):
    """
    Raw Data Config –
        This configuration file is automatically loaded when placed in the raw_data directory,
        using its filename as the attribute name DO NOT INCLUDE THE _path, can also be loaded using environment variables.

    Attributes:
        prospects_path: The prospects CSV file location.
        country_to_region_mapping_path: The country to region JSON file location.
        user_locations_settings_path: The user location settings JSON file.
    """
    prospects_path: str = "./raw_data/prospects.csv"
    country_to_region_mapping_path: str = "./raw_data/country-to-regions-mapping.json"
    user_locations_settings_path: str = "./raw_data/users-locations-settings.json"
