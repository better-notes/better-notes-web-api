from typing import Any, Dict

from web_api import commons


class ListNoteSpecification(commons.specs.Specification):
    def get_query(self) -> Dict[str, Any]:
        return {}
