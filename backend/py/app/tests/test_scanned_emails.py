from fastapi.testclient import TestClient
from unittest import mock

from app.crud import crud_user, crud_linked_emails, crud_unsubscribe_links
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

        # Add a linked_email account
        linked_email = crud_linked_emails.linked_email.create_with_user(
            self.session,
            obj_in=LinkedEmailsCreate(
                email="email@yahoo.com",
                password="a-super-secret-password",
            ),
            user_id=self.user.id,
        )

        # Generate 20 test spam emails and scan them
        for i in range(20):
            message = generate_email_message(
                to_email="email@yahoo.com",
                from_email="spammer@email.com",
                subject=f"Spam Email - {i}",
                body=general_template,
            )
            EmailUnsubscriber._scan_email_message_obj(
                db=self.session,
                email_msg=message,
                linked_email_address=linked_email.email,
            )

        # Fetch the list of scanned_emails for page 0
        results = self.client.get(
            "/scanned_emails/scanned_emails/0",
            headers=self.auth_header,
        ).json()
        scanned_emails = results.get("scanned_emails", [])

        expected_scanned_emails_page_0 = [
            {
                "email_from": "spammer@email.com",
                "id": mock.ANY,
                "link_count": 1,
                "linked_email_address": "email@yahoo.com",
                "subject": f"Spam Email - {i}",
            }
            for i in range(10)
        ]
        assert scanned_emails == expected_scanned_emails_page_0

        # Fetch the list of scanned emails for page 1
        # it should contain the rest of the scanned emails
        results = self.client.get(
            "/scanned_emails/scanned_emails/1?linked_email=email@yahoo.com",
            headers=self.auth_header,
        ).json()
        scanned_emails2 = results.get("scanned_emails", [])

        expected_scanned_emails_page_1 = [
            {
                "email_from": "spammer@email.com",
                "id": mock.ANY,
                "link_count": 1,
                "linked_email_address": "email@yahoo.com",
                "subject": f"Spam Email - {i}",
            }
            for i in range(10, 20)
        ]
        assert scanned_emails2 == expected_scanned_emails_page_1

        # Fetch the list of scanned emails for page 2
        # it should not contain anymore emails.
        results = self.client.get(
            "/scanned_emails/scanned_emails/2",
            headers=self.auth_header,
        ).json()
        scanned_emails3 = results.get("scanned_emails", [])
        assert scanned_emails3 == []

        # Fetch a list of unsubscribe links for a certain scanned_email_id and linked_email
        scanned_email_id = scanned_emails2[0].get("id")
        results = self.client.get(
            f"/unsubscribe_links/unsubscribe_links_by_email/{scanned_email_id}/?linked_email=email@yahoo.com",
            headers=self.auth_header,
        ).json()

        expected_unsuscribe_links = [
            {
                "scanned_email_id": scanned_email_id,
                "id": mock.ANY,
                "link": "https://github.com/konsav/email-templates/",
                "unsubscribe_status": "pending",
                "insert_ts": mock.ANY,
                "linked_email_address": "email@yahoo.com",
            }
        ]

        assert results.get("links", []) == expected_unsuscribe_links
