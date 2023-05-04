from fastapi.testclient import TestClient
from unittest import mock

from app.crud import crud_user, crud_linked_emails, crud_scanned_emails
from app.main import app
from app.objects.email_unsubscriber import EmailUnsubscriber
from app.schemas import LinkedEmailsCreate
from app.test_utils import (
    get_session,
    generate_user,
    generate_auth_header,
    generate_email_message,
)
from app.tests.html_emails.basic_promo import basic_promo
from app.tests.html_emails.general_template import general_template


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

    # This mock ensures we don't actually try to login to this user's email
    @mock.patch(
        "app.objects.email_unsubscriber.IMAP4_SSL.login",
        return_value=True,
        autospec=True,
    )
    def test_get_scanned_emails(self, mock_imap_login) -> None:
        """Test linking an email to a user account

        Routes tested:
            /linked_emails/link_email
        """
        linked_email = crud_linked_emails.linked_email.create_with_user(
            self.session,
            obj_in=LinkedEmailsCreate(
                email="email@yahoo.com",
                password="a-super-secret-password",
            ),
            user_id=self.user.id,
        )

        for idx, html_email in enumerate((basic_promo, general_template)):
            message = generate_email_message(
                to_email="email@yahoo.com",
                from_email="spammer@email.com",
                subject=f"Spam Email - {idx}",
                body=html_email,
            )
            EmailUnsubscriber._scan_email_message_obj(
                db=self.session,
                email_msg=message,
                linked_email_address=linked_email.email,
            )
        scanned_emails = crud_scanned_emails.scanned_emails.get_scanned_emails(
            db=self.session,
        )
        from pprint import pprint

        pprint(scanned_emails)

        # TODO: Test the scanned_emails data
        # TODO: Add a crud_unsubscribe_links and test retrieval
