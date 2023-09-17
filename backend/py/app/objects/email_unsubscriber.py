import email
import os
import quopri
import re
import requests
import lxml.html

from datetime import datetime
from sqlalchemy.orm import Session
from email.header import decode_header
from email.message import Message
from email.header import Header
from email.utils import parsedate_to_datetime
from fastapi import HTTPException
from imaplib import IMAP4_SSL
from typing import List, Tuple, Union

from app.models import ScannedEmails, UnsubscribeLinks, UnsubscribeStatus


class EmailUnsubscriber:
    """Email Unsubscriber Class"""

    UNSUBSCRIBE_KEYWORDS = [
        "unsubscribe",
        "[unsubscribe]",
        "exclude",
        "opt-out",
        "opt out",
        "if you no longer wish to receive this email",
        "subscription",
    ]
    SUPPORTED_IMAP_SERVERS = {
        "yahoo": "imap.mail.yahoo.com",
        "google": "imap.gmail.com",
    }

    def __init__(self, email_type: str) -> None:
        """Connect to the email's imap server by email_type.

        Args:
            email_type (str): The email type.

        Raises:
            Exception: If email_type is not supported.
        """
        if email_type not in self.SUPPORTED_IMAP_SERVERS:
            raise HTTPException(
                status_code=400, detail=f"{email_type} is not a supported email yet."
            )

        self.email_type = email_type
        self.email = None

        # Now login to the imap server
        imap_server = self.SUPPORTED_IMAP_SERVERS[email_type]
        self.imap = IMAP4_SSL(imap_server)

        self.unsubscriber_info: List[dict] = []

    def __del__(self) -> None:
        """Disconnect from the imap server upon calling the destructor."""
        self.logout()

    def logout(self) -> None:
        """Logout of the imap server."""
        if hasattr(self, "imap") and self.imap.state != "LOGOUT":
            self.imap.logout()

    def login(self, email_username: str, email_password: str) -> bool:
        """Login to the imap server with the passed in username and password.

        Args:
            email_username (str): The email username. Must be in the form 'x@example.com'
            email_password (str): The password.

        Raises:
            Exception: If email is in incorrect format
            Exception: If username and password is incorrect.
        """
        if not re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_username
        ):
            # Raise exception if email is in the incorrect format.
            raise HTTPException(
                status_code=400,
                detail=f"Email: '{email_username}' not in correct format",
            )

        # NOTE: Can raise Exception if email_username and password is incorrect.
        try:
            self.imap.login(email_username, email_password)
            self.email = email_username
        except:
            return False
        return True

    def get_domain_from_email(email_address: str) -> str:
        """Get an email address domain from an email address

        Args:
            email_address (str): the email address

        Returns:
            str: The email domain
        """
        # Get the email domain
        domain_match = re.search(r"@[\w\-]+", email_address)
        if not domain_match:
            raise HTTPException(
                status_code=400,
                detail=f"Could not find email domain for email: {email_address}",
            )

        # Chop off the '@'
        domain = domain_match.group()[1:]
        return domain

    def get_unsubscribe_links_from_inbox(
        self, db: Session, how_many: int = None, order_by: str = "desc"
    ) -> List[dict]:
        """Iterate through the Inbox looking through the email body for
        words in `self.UNSUBSCRIBE_KEYWORDS`.
        If one of the keywords is found in the email body we look for a
        possible link that is following the position of said found keyword.

        Args:
            db (Session): The db session
            how_many (int, optional): Number of emails to fetch from inbox descending.
                Defaults to all emails in the Inbox.
            order_by (str, optional): Method of getting the emails, i.e. 'desc', 'asc'.
                Defaults to 'desc'.

        Returns:
            List[dict]: A list of data describing the emails scanned in this format.
                [
                    {
                        "id": 52,
                        "from": "sender@spam.mail.com",
                        "subject": "subject of email",
                        "link_count": 3
                    },
                    ...
                ]
        """

        # Throttle to 30 emails at once.
        # TODO make this a background task to allow for scanning more emails.
        if how_many > 30:
            raise HTTPException(
                status_code=400,
                detail="Error you can not scan more than 30 emails at a time"
            )

        # Readonly does not mark emails as SEEN
        status, messages = self.imap.select("INBOX", readonly=True)
        if status != "OK":
            raise HTTPException(
                status_code=400,
                detail=f"Could not select Inbox...\tGot status: {status}",
            )

        # If the inbox retrieval is successful but there are no emails
        # we can return early.
        if not messages or not messages[0] or not int(messages[0]):
            return

        number_of_emails = int(messages[0])

        # set how we fetch and order getting the emails.
        range_params: tuple = ()
        if order_by == "desc":
            how_many = how_many or 0
            range_params = (number_of_emails, number_of_emails - how_many, -1)
        elif order_by == "asc":
            how_many = how_many or number_of_emails
            range_params = (0, how_many)
        else:
            how_many = how_many or number_of_emails
            range_params = (how_many, 0, -1)

        # We can't fetch more emails than exist in the Inbox.
        if how_many > number_of_emails:
            raise HTTPException(
                status_code=400,
                detail="how_many can't be greater than total number of emails in Inbox:"
                f" {number_of_emails}",
            )

        # TODO? Turn these into logs
        print("Fetching emails...")
        current_iteration = 0
        # print_progress(
        #     current_iteration=current_iteration,
        #     total=how_many,
        #     prefix="Progress:",
        #     suffix="Complete",
        # )
        scanned_emails = []
        for i in range(*range_params):
            response, msg = self.imap.fetch(str(i), "(RFC822)")

            if response != "OK":
                raise Exception(f"Unable to fetch email: {i}\Response: {response}")

            # Get the email as an email object
            email_msg = email.message_from_bytes(msg[0][1])

            # Get the time the email was added to the inbox.
            status, data = self.imap.fetch(str(i), "(INTERNALDATE)")

            if response != "OK":
                raise Exception(f"Unable to fetch INTERNALDATE for email: {i}")
            
            str_datetime = data[0].decode().split('"')[1]
            datetime_obj = parsedate_to_datetime(str_datetime)

            # Scan the email Message object
            scanned_email = self._scan_email_message_obj(db, email_msg, self.email, datetime_obj)

            if scanned_email:
                scanned_emails.append(scanned_email)

            current_iteration += 1
            # print_progress(
            #     current_iteration=current_iteration,
            #     total=how_many,
            #     prefix="Progress:",
            #     suffix="Complete",
            # )

        # Close the INBOX
        self.imap.close()
        return scanned_emails

    @classmethod
    def _scan_email_message_obj(
        cls, db: Session, email_msg: Message, linked_email_address: str, inbox_date: datetime,
    ) -> dict:
        """Scan an email message object. Here we get the message sender info such as
        the email subject and who it's being sent from. Then scan the actual email content
        for links and if we found some add them to the database.
        This is a classmethod so that this method can be used for testing.

        Args:
            db (Session): The db session object.
            email_message (Message): The email message object.
            linked_email_address (Str): The email address of the recipient
            inbox_date (datetime): The time the email was added to the inbox

        Returns:
            dict: The id, email_from, subject and unsubscribe link count
                {
                    "id": 52,
                    "from": "sender@spam.mail.com",
                    "subject": "subject of email",
                    "link_count": 3,
                    "unsubscribe_status": "pending",
                },
        """
        # Get the email sender and convert from bytes if necessary
        email_from, email_subject = cls.decode_from_and_subject(
            email_msg["From"], email_msg["Subject"]
        )

        # Don't add scanned emails that already exist
        existing_email = (
            db.query(ScannedEmails)
            .filter(
                ScannedEmails.email_from == email_from,
                ScannedEmails.subject == email_subject,
                ScannedEmails.inbox_date == inbox_date,
            )
            .first()
        )

        if existing_email:
            return {}

        # Insert the scanned_email info into the db.
        scanned_email = ScannedEmails(
            email_from=email_from,
            subject=email_subject,
            linked_email_address=linked_email_address,
            inbox_date=inbox_date,
        )
        db.add(scanned_email)
        db.flush()

        # Get unsubscribe links
        unsubscribe_links = cls._get_unsubscribe_links_from_email(
            email_msg, email_subject
        )

        # Add all unsubscribe links to the unsubscribe_links table
        unsubscribe_link_objs = []
        for link in unsubscribe_links:
            unsubscribe_link_objs.append(
                UnsubscribeLinks(
                    link=link,
                    unsubscribe_status=UnsubscribeStatus.pending,
                    linked_email_address=linked_email_address,
                    scanned_email_id=scanned_email.id,
                )
            )
        db.add_all(unsubscribe_link_objs)
        db.flush()
        db.commit()
        return {
            "id": scanned_email.id,
            "from": email_from,
            "subject": email_subject,
            "link_count": len(unsubscribe_link_objs),
            "unsubscribe_status": "pending",
        }

    @staticmethod
    def decode_from_and_subject(
        email_from: Header = None, email_subject: Header = None
    ) -> Tuple[str, str]:
        """Decode the from and subject.

        Args:
            email_from (Header, optional): Email From Header. Defaults to None.
            email_subject (Header, optional): Email Subject. Defaults to None.

        Returns:
            Tuple[str, str]: The email_from and email_subject
        """
        email_from_bytes, from_encoding = decode_header(email_from)[0]
        email_subject_bytes, subject_encoding = decode_header(email_subject)[0]

        # Decode the email_from and email_subject from bytes. We do this by doing
        # a series of checks:
        #
        #   1. If the from/subject is of type bytes we decode it from the given
        #       encoding.
        #   2. The encoding may have not been returned from decode_header().
        #       In this case we can just perform a type conversion to string.
        #
        if isinstance(email_from_bytes, bytes) and from_encoding:
            email_from_str = email_from_bytes.decode(from_encoding)
        else:
            email_from_str = str(email_from_bytes)

        if isinstance(email_subject_bytes, bytes) and subject_encoding:
            email_subject_str = email_subject_bytes.decode(subject_encoding)
        else:
            email_subject_str = str(email_subject_bytes)

        return email_from_str, email_subject_str

    @classmethod
    def _get_unsubscribe_links_from_email(
        cls, email_msg: Message, email_subject: str
    ) -> List[str]:
        """Takes an email message object and parses the body to find links
        that will (hopefully) unsubscribe us from the email.

        Args:
            email_msg (Message): The email Message object.
            email_subject (str): The email subject. Printed to the console
             if decoding the email fails.

        Returns:
            List[str]: A list of possible unsubscribe links from the email Message.
        """
        unsubscribe_links = []

        # A multipart email message may contain both a text/plain AND text/html email.
        if email_msg.is_multipart():
            for part in email_msg.walk():
                # Get the Content-Type
                content_type = part.get_content_type()
                body = part.get_payload()

                # Parse a text/plain email
                if content_type == "text/plain":
                    try:
                        body = quopri.decodestring(body).decode(
                            "utf-8", errors="ignore"
                        )
                    except Exception as e:
                        # TODO: Log here
                        # print_warning(
                        #     f"Was unable to decode body for email: {email_subject}\nError: {e}"
                        # )
                        continue
                    found_links = cls._get_unsubscribe_links_from_text_plain(body=body)

                    # Don't add duplicate links
                    for link in found_links:
                        if link not in unsubscribe_links:
                            unsubscribe_links.append(link)

                # Parse a text/html email
                elif content_type == "text/html":
                    try:
                        body = quopri.decodestring(body).decode(
                            "utf-8", errors="ignore"
                        )
                    except Exception as e:
                        # TODO: Log here
                        # print_warning(
                        #     f"Was unable to decode body for email: {email_subject}\nError: {e}"
                        # )
                        continue
                    found_links = cls._get_unsubscribe_links_from_html(body=body)

                    # Don't add duplicate links
                    for link in found_links:
                        if link not in unsubscribe_links:
                            unsubscribe_links.append(link)

        # When the email is not multipart we can pass decode=True to get_payload() to decode the email for us.
        else:
            content_type = email_msg.get_content_type()
            body = email_msg.get_payload(decode=True).decode("utf-8", "replace")

            if content_type == "text/plain":
                unsubscribe_links = cls._get_unsubscribe_links_from_text_plain(
                    body=body
                )
            elif content_type == "text/html":
                unsubscribe_links = cls._get_unsubscribe_links_from_html(body=body)

        return unsubscribe_links

    @classmethod
    def _get_unsubscribe_links_from_html(cls, body: str) -> list:
        """Look for unsubscribe links in the body of the email
        as an html email.

        Args:
            body (str): The body of the email.

        Returns:
            list: The unsubscribe links found.
        """
        unsubscribe_links = []

        # Scrub the html by removing \n and \r characters
        html = body.replace("\n", "").replace("\r", "")

        # Parse the html using lxml
        element_tree = lxml.html.fromstring(html)

        # Get html <a> elements that only contain unsubscribe keywords
        # For example <a href="https://example_link.com/unsub_from_me">unsubscribe</a>
        for unsub_keyword in cls.UNSUBSCRIBE_KEYWORDS:
            # Semi HACK way of checking for upper case characters, use .title()
            link_elements = element_tree.xpath(
                f'.//a[contains(text(), "{unsub_keyword}")]'
            ) or element_tree.xpath(
                f'.//a[contains(text(), "{unsub_keyword.title()}")]'
            )

            # If any links are found get them by accessing the 'href' attribute
            if link_elements is not None and isinstance(link_elements, list):
                for element in link_elements:
                    found_link = element.attrib.get("href")

                    if found_link and found_link not in unsubscribe_links:
                        unsubscribe_links.append(found_link)

        return unsubscribe_links

    @classmethod
    def _get_unsubscribe_links_from_text_plain(cls, body: str) -> list:
        """Look for unsubscribe links in the body of the email as a
        plain text email.

        Args:
            body (str): The body of the email.

        Returns:
            list: The unsubscribe links found.
        """
        unsubscribe_links = []

        # Look for unsubscribe keywords, some emails have totally different keywords used for their unsubscribe hyperlinks.
        for unsub_keyword in cls.UNSUBSCRIBE_KEYWORDS:
            unsub_idx = body.lower().find(unsub_keyword)

            if unsub_idx != -1:
                # Remove \n and \r characters out of the body to sanitize the link.
                trimmed_body = body[unsub_idx:].replace("\n", "").replace("\r", "")

                # Get the link following the unsubscribe keyword
                match = re.search(
                    r"(?:(?:https?):\/\/)[\w/\-?=%~.]+\.[\w/\-&?=%~]+",
                    trimmed_body,
                )

                # If we've found the link check first to make sure we haven't found this link already.
                if match and match.group() not in unsubscribe_links:
                    unsubscribe_links.append(match.group())

        return unsubscribe_links
