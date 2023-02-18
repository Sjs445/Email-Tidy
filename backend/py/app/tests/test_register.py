from fastapi.testclient import TestClient

from app.crud import crud_user
from app.main import app
from app.schemas.users import UserCreate
from app.test_utils import get_session


class TestRegister:
    """Test register class"""

    def setup_method(self) -> None:
        self.user_id = None
        self.user_email = None
        self.client = TestClient(app)
        self.session = get_session()

    def teardown_method(self) -> None:
        if self.user_id is not None:
            crud_user.user.remove(self.session, id=self.user_id, email=self.user_email)
        self.session.close()

    def test_register(self) -> None:
        """Test registering a user and making sure their account
        is in the db.

        Routes Tested:
            /users/register
        """
        self.user_email = "bob@email.com"
        response: dict = self.client.post(
            "/users/register",
            json={
                "email": self.user_email,
                "password": "123abc!@",
                "first_name": "bob",
                "last_name": "doe",
            },
        ).json()
        self.user_id = response.get("id")
        assert self.user_id is not None
        assert isinstance(self.user_id, int)
        user = crud_user.user.get_by_email(self.session, email=self.user_email)
        assert user.id == self.user_id

    def test_login(self) -> None:
        """Test logging in a user.

        Routes Tested:
            /login/access-token
            /login/test-token
        """
        self.user_email = "bobdoe@email.com"

        # Create a user account.
        user = crud_user.user.create(
            self.session,
            obj_in=UserCreate(
                email=self.user_email,
                first_name="bob",
                last_name="doe",
                password="mysupersecretpassword",
            ),
        )
        self.user_id = user.id

        # Login to get an access token
        response = self.client.post(
            "/login/access-token",
            data={
                "username": self.user_email,
                "password": "mysupersecretpassword",
            },
        )
        tokens = response.json()
        assert "access_token" in tokens
        header = {"Authorization": f"Bearer {tokens.get('access_token')}"}

        # Test that access token
        res = self.client.post(
            "/login/test-token",
            headers=header,
        )
        assert res.status_code == 200
        user_data = res.json()
        assert user_data.get("email") == self.user_email
        assert user_data.get("id") == self.user_id
