from fastapi.testclient import TestClient

from app.crud import crud_user
from app.main import app
from app.models.invite_codes import InviteCodes
from app.schemas.users import UserCreate
from app.test_utils import get_session
from app.utils import generate_invite_code

class TestRegister:
    """Test register class"""

    def setup_method(self) -> None:
        self.user_id = None
        self.user_email = None
        self.invite_code = None
        self.client = TestClient(app)
        self.session = get_session()

    def teardown_method(self) -> None:
        if self.invite_code is not None:
            code = (
                self.session.query(InviteCodes)
                .filter(InviteCodes.code == self.invite_code)
                .first()
            )
            self.session.delete(code)
            self.session.commit()
        
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
        register_params = {
            "email": self.user_email,
            "password": "123abc!@",
            "first_name": "bob",
            "last_name": "doe",
        }

        # Try and register without an invite code
        response: dict = self.client.post(
            "/users/register",
            json=register_params,
        ).json()
        assert response.get("detail") == [{'loc': ['body', 'invite_code'], 'msg': 'field required', 'type': 'value_error.missing'}]

        # Try and register with invalid password format
        register_params["invite_code"] = "123abc"
        response: dict = self.client.post(
            "/users/register",
            json=register_params,
        ).json()
        assert response.get("detail") == "Password must have uppercase: 1 "

        # Register with an invalid invite code
        register_params["password"] = "123Abc!@"
        response: dict = self.client.post(
            "/users/register",
            json=register_params,
        ).json()
        assert response.get("detail") == "Invalid invite code"

        self.invite_code, ts = generate_invite_code(self.session, 1)
        register_params["invite_code"] = self.invite_code

        # Actually register witha valid invite code
        response: dict = self.client.post(
            "/users/register",
            json=register_params,
        ).json()
        
        access_token = response.get("access_token")
        assert isinstance(access_token, str)
        user = crud_user.user.get_by_email(self.session, email=self.user_email)
        self.user_id = user.id
        assert user.id == self.user_id

    def test_login(self) -> None:
        """Test logging in a user.

        Routes Tested:
            /login/access-token
            /login/test-token
        """
        self.user_email = "bobdoe@email.com"

        # Create a user account.
        self.invite_code, ts = generate_invite_code(self.session, expires_in=1)
        user = crud_user.user.create(
            self.session,
            obj_in=UserCreate(
                email=self.user_email,
                first_name="bob",
                last_name="doe",
                password="mysupersecretpassword",
                invite_code=self.invite_code
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
