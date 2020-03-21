from yoyo import step
__depends__ = {'0013.drop-misc'}
step(
    """CREATE TABLE misc(
        note_id integer REFERENCES note(id),
        tags_id integer REFERENCES tags(id)
        ON DELETE CASCADE
    )"""
)
