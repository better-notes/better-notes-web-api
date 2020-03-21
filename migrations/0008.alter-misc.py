from yoyo import step
__depends__ = {'0007.alter-notes'}
step(
    """ALTER TABLE misc
    RENAME COLUMN notes_id TO note_id"""
)
