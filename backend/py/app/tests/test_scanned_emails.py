from fastapi.testclient import TestClient
from unittest import mock
from datetime import datetime

from app.crud import crud_user, crud_linked_emails
from app.main import app
from app.objects.email_unsubscriber import EmailUnsubscriber
from app.schemas import LinkedEmailsCreate
from app.test_utils import (
    get_session,
    generate_user,
    generate_auth_header,
    generate_email_message,
)
from app.tests.html_emails.general_template import general_template


class TestLinkEmail:
    """Test link email class"""

    @classmethod
    def setup_class(cls) -> None:
        cls.client = TestClient(app)
        cls.session = get_session()
        cls.user = generate_user(cls.session)
        cls.auth_header = generate_auth_header(cls.user.id)
        cls.list_unsubscribe = [ f'<https://example.com/unsubscribe_me/{i}>' for i in range(20) ]

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
                list_unsubscribe=[self.list_unsubscribe[i]],
            )
            EmailUnsubscriber._scan_email_message_obj(
                db=self.session,
                email_msg=message,
                linked_email_address=linked_email.email,
                inbox_date=datetime.now(),
            )

        # Fetch the list of scanned_emails for page 0
        scanned_email_params = {
            "linked_email": "email@yahoo.com",
            "email_from": "spammer@email.com",
            "page": 0,
        }
        results = self.client.post(
            "/scanned_emails/get_scanned_emails",
            json=scanned_email_params,
            headers=self.auth_header,
        ).json()
        scanned_emails = results.get("scanned_emails", [])

        expected_scanned_emails_page_0 = [
            {
                "id": mock.ANY,
                "unsubscribe_link_count": 1,
                "subject": f"Spam Email - {i}",
                "total_count": 20,
                "unsubscribe_statuses": ["pending"],
            }
            for i in range(10)
        ]

        # frozenset allows for testing without order.
        assert [ frozenset(email) for email in scanned_emails ] == [ frozenset(email) for email in expected_scanned_emails_page_0 ]

        # Fetch the list of scanned emails for page 1
        # it should contain the rest of the scanned emails
        scanned_email_params["page"] = 1
        results = self.client.post(
            "/scanned_emails/get_scanned_emails",
            json=scanned_email_params,
            headers=self.auth_header,
        ).json()
        scanned_emails2 = results.get("scanned_emails", [])

        expected_scanned_emails_page_1 = [
            {
                "id": mock.ANY,
                "unsubscribe_link_count": 0,
                "subject": f"Spam Email - {i}",
                "unsubscribe_statuses": None,
                "total_count": 20,
            }
            for i in range(10, 20)
        ]
        assert [ frozenset(link) for link in scanned_emails2 ] == [ frozenset(link) for link in expected_scanned_emails_page_1 ]

        # Fetch the list of scanned emails for page 2
        # it should not contain anymore emails.
        scanned_email_params["page"] = 2
        results = self.client.post(
            "/scanned_emails/get_scanned_emails",
            json=scanned_email_params,
            headers=self.auth_header,
        ).json()
        scanned_emails3 = results.get("scanned_emails", [])
        assert scanned_emails3 == []

        # Fetch a list of unsubscribe links for a certain scanned_email_id and linked_email
        scanned_email_id = scanned_emails[0].get("id")
        results = self.client.get(
            f"/unsubscribe_links/unsubscribe_links_by_email/{scanned_email_id}/?linked_email=email@yahoo.com",
            headers=self.auth_header,
        ).json()

        expected_unsuscribe_links = [
            {
                "scanned_email_id": scanned_email_id,
                "id": mock.ANY,
                "link": self.list_unsubscribe[0].strip('<>'),
                "unsubscribe_status": "pending",
                "insert_ts": mock.ANY,
                "linked_email_address": "email@yahoo.com",
            }
        ]

        assert results.get("links", []) == expected_unsuscribe_links

        # Fetch a list of email senders
        results = self.client.get(
            "/scanned_emails/senders/0?linked_email=email@yahoo.com",
            headers=self.auth_header,
        ).json()

        assert results.get("senders", []) == [
            {
                "email_from": "spammer@email.com",
                "scanned_email_count": 20,
                "unsubscribe_link_count": 20,
                "total_count": 1,
                "unsubscribe_statuses": ["pending" for _ in range(20)],
            }
        ]
