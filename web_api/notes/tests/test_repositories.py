import pytest
from motor import motor_asyncio
from snapshottest.pytest import PyTestSnapshotTest

from web_api.notes import repositories
from web_api.notes.tests import factories


class TestNoteRepository:
    @pytest.mark.asyncio  # type: ignore
    async def test_add(
        self,
        motor_client: motor_asyncio.AsyncIOMotorClient,
        snapshot: PyTestSnapshotTest,
    ) -> None:
        # Given
        note = factories.NoteValueFactory()
        repository = repositories.NoteRepository(client=motor_client)
        # When
        result = await repository.add(note)
        # Then
        snapshot.assert_match(result.as_dict())
