from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    """
    Postgres configuration

    Attributes:
        postgres_user: The username used to connect to the Postgres database.
        postgres_password: The password used to connect to the Postgres database.
        postgres_host: The host used to connect to the Postgres database.
    """
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"