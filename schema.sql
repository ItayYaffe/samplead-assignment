CREATE TABLE prospect_qualifications (
    id              SERIAL PRIMARY KEY,

    user_id         TEXT NOT NULL,
    prospect_id     TEXT NOT NULL,

    qualifies       BOOLEAN NOT NULL,

    matched_by      TEXT,
    matched_with     TEXT CHECK (matched_with IN ('DIRECT', 'REGION', 'NONE')),

    evaluated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (user_id, prospect_id)
);
