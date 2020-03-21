from yoyo import step
step(
    """CREATE TABLE tag(
    id integer NOT NULL UNIQUE,
    created_at timestamp with time zone,
    name text,
    PRIMARY KEY(id)
    );""",
)
