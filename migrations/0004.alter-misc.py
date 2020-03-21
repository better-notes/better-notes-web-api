from yoyo import step
__depends__ = {'0003.create-misc'}
step(
    """ALTER TABLE misc ADD CONSTRAINT notes_tag_unique_together UNIQUE
    (notes_id, tag_id)"""
)
