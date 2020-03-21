from yoyo import step
step(
    """CREATE TABLE note(
    id SERIAL NOT NULL UNIQUE,
    text TEXT,
    created_at timestamp with time zone,
    PRIMARY KEY(id)
    );""",
)