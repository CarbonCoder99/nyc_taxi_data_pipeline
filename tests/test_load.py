import os
import pytest

from scripts.load import get_db_url


def test_get_db_url_requires_env(monkeypatch):
    monkeypatch.delenv("DB_URL", raising=False)
    with pytest.raises(ValueError):
        get_db_url()
