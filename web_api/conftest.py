import pytest
import factory


@pytest.fixture(autouse=True, scope='function')  # type: ignore
def reset_sequence() -> None:
    """Reset any factory sequence before each test start."""
    for factory_ in factory.Factory.__subclasses__():
        factory_.reset_sequence(0)
