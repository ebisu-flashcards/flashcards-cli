import pytest

from flashcards_core.database import init_db


@pytest.fixture()
def session(monkeypatch, tmpdir):
    session_maker = init_db(database_path=f"sqlite:///{tmpdir}/sqlite_test.db")
    with session_maker() as db:
        yield db
