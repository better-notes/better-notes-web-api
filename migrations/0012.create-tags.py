from yoyo import step
step(
    """CREATE TABLE tags(
    id SERIAL NOT NULL UNIQUE,
    created_at timestamp with time zone,
    name TEXT,
    PRIMARY KEY(id)
    );""",
)
