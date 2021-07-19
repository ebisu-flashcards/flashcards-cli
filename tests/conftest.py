import pytest

import flashcards_core
from flashcards_core.database import SessionLocal


@pytest.fixture
def session():
    with SessionLocal() as db:
        yield db


@pytest.fixture
def temp_db(monkeypatch, tmpdir):
    monkeypatch.setattr(flashcards_core.database, "SQLALCHEMY_DATABASE_URL", tmpdir)
