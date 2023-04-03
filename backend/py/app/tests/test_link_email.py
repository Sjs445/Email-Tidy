from fastapi.testclient import TestClient
from unittest import mock

from app.crud import crud_user, crud_linked_emails
from app.main import app
from app.test_utils import get_session, generate_user, generate_auth_header
from app.config.security import decrypt_email_password


class TestLinkEmail:
    """Test link email class"""

    @classmethod
    def setup_class(cls) -> None:
        cls.client = TestClient(app)
        cls.session = get_session()
        cls.user = generate_user(cls.session)
        cls.auth_header = generate_auth_header(cls.user.id)

    @classmethod
    def teardown_class(cls) -> None:
        if cls.user is not None:
            crud_user.user.remove(cls.session, id=cls.user.id, email=cls.user.email)
        cls.session.close()

    # This mock ensures we don't actually try to login to this email address
    @mock.patch(
        "app.objects.email_unsubscriber.IMAP4_SSL.login",
        return_value=True,
        autospec=True,
    )
    def test_link_email(self, mock_imap_login) -> None:
        """Test linking an email to a user account

        Routes tested:
            /linked_emails/link_email
        """
        response = self.client.post(
            "/linked_emails/link_email",
            json={
                "email": "email@yahoo.com",
                "password": "123abcmnbiou",
            },
            headers=self.auth_header,
        ).json()
        assert response.get("success")

        linked_email = crud_linked_emails.linked_email.get_by_email(
            self.session, email="email@yahoo.com"
        )
        assert decrypt_email_password(linked_email.password) == "123abcmnbiou"

    def test_get_linked_emails(self) -> None:
        """Test getting a list of currently linked_emails

        Routes tested:
            /linked_emails/linked_emails
        """
        response = self.client.get(
            "/linked_emails/linked_emails",
            headers=self.auth_header,
        ).json()
        assert response.get("linked_emails") == [
            {"email": "email@yahoo.com", "id": mock.ANY, "is_active": True}
        ]
