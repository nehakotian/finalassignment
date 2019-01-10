import pytest
import main
import flask
from main import *
from flask.testing import FlaskClient
from main import db as _db

# Connection to the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:neha@localhost/studentclass'
app.config['SECRET_KEY'] = "nrkotian"
db = SQLAlchemy(app)
main.db.create_all()


@pytest.fixture(scope='module')
def test_resp_code():
    client = main.app.test_client()
    return client
