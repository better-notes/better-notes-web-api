from yoyo import step
step(
    """CREATE TABLE misc(
        notes_id integer REFERENCES notes(id),
        tag_id integer REFERENCES tag(id)
        UNIQUE (notes_id, tag_id));"""
)
