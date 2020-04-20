# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from unittest.mock import ANY

from snapshottest import GenericRepr, Snapshot

snapshots = Snapshot()

snapshots['TestCreateNoteView.test_post[pyloop] 1'] = [
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
    }
]
