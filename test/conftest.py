import os
import pytest

from flaskapp import create_app

# To be added later: db as _db

TESTDB = 'test_project.db'
TESTDB_PATH = "/opt/project/data/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite://' + TESTDB_PATH


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = create_app(__name__, settings_override)
 
    with app.test_client() as client:
        yield client

