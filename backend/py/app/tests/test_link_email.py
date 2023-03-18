from fastapi.testclient import TestClient
from unittest import mock

from app.crud import crud_user, crud_linked_emails
from app.main import app
from app.test_utils import get_session, generate_user, generate_auth_header
from app.config.security import decrypt_email_password


class TestLinkEmail:
    """Test link email class"""

    def setup_method(self) -> None:
        self.client = TestClient(app)
        self.session = get_session()
        self.user = generate_user(self.session)
        self.auth_header = generate_auth_header(self.user.id)

    def teardown_method(self) -> None:
        if self.user is not None:
            crud_user.user.remove(self.session, id=self.user.id, email=self.user.email)
        self.session.close()

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
