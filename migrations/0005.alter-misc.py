from yoyo import step
__depends__ = {'0004.alter-misc'}
step(
    """ALTER TABLE misc
    DROP CONSTRAINT misc_notes_id_fkey,
    ADD CONSTRAINT misc_notes_id_fkey FOREIGN KEY (notes_id)
    REFERENCES notes (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

    ALTER TABLE misc
    DROP CONSTRAINT misc_tag_id_fkey,
    ADD CONSTRAINT misc_tag_id_fkey FOREIGN KEY (tag_id)
    REFERENCES tag (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;"""
)
