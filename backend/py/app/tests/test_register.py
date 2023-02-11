from fastapi.testclient import TestClient

from app.main import app


class TestRegister:
    """Test a user can register"""

    def setup_method(self):
        self.client = TestClient(app)
        pass

    def teardown_method(self):
        pass

    def test_register(self):
        # TODO
        assert 1 == 1
