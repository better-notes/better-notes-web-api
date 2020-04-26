# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot
from unittest.mock import ANY


snapshots = Snapshot()

snapshots['TestNoteInteractor.test_add_get[pyloop] 1'] = [
    {
        'created_at': GenericRepr(ANY),
        'id_': {'value': GenericRepr(ANY)},
        'tags': [
            {
                'created_at': GenericRepr(ANY),
                'id_': {'value': GenericRepr(ANY)},
                'name': 'tag #0',
            }
        ],
        'text': 'Sample text',
    },
    {
        'created_at': GenericRepr(ANY),
        'id_': {'value': GenericRepr(ANY)},
        'tags': [
            {
                'created_at': GenericRepr(ANY),
                'id_': {'value': GenericRepr(ANY)},
                'name': 'tag #1',
            }
        ],
        'text': 'Sample text',
    },
    {
        'created_at': GenericRepr(ANY),
        'id_': {'value': GenericRepr(ANY)},
        'tags': [
            {
                'created_at': GenericRepr(ANY),
                'id_': {'value': GenericRepr(ANY)},
                'name': 'tag #2',
            }
        ],
        'text': 'Sample text',
    },
]
