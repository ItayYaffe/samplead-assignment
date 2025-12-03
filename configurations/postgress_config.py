from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    """
    Postgres configuration

    Attributes:
        postgres_dsn: Postgres DSN
    """
    postgres_dsn: str = "postgresql://postgres:postgres@localhost:5432/app_db"


POSTGRES_INSERT_QUERY = """
                        INSERT INTO prospect_qualifications (user_id,
                                                             prospect_id,
                                                             qualifies,
                                                             matched_with,
                                                             matched_by,
                                                             evaluated_at)
                        VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT (user_id, prospect_id) DO
                        UPDATE
                            SET
                                qualifies = EXCLUDED.qualifies,
                            matched_with = EXCLUDED.matched_with,
                            matched_by = EXCLUDED.matched_by,
                            evaluated_at = EXCLUDED.evaluated_at; \
                        """
