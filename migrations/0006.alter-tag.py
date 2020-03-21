from yoyo import step
__depends__ = {'0005.alter-misc'}
step(
    """ALTER TABLE tag RENAME TO tags"""
)
