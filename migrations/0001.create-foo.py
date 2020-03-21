from yoyo import step
step(
    """CREATE TABLE notes(
    id integer NOT NULL UNIQUE,
    text text,
    created_at timestamp with time zone,
    PRIMARY KEY(id)
    );""",
)