from yoyo import step
__depends__ = {'0006.alter-tag'}
step(
    """ALTER TABLE notes RENAME TO note"""
)