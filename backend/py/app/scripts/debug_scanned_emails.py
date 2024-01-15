#!/usr/bin/env python3
"""This script serves as a way to debug scanned emails that cause errors.

The script accepts these params:
-l --linked_email (Str) the linked email to test on
--how_many [Optional] (Int) the number of emails to scan.
-h --help (Bool) prints the help message for this script
"""

import argparse

from app.config import security
from app.database.database import SessionLocal
from app.models.linked_emails import LinkedEmails
from app.objects.email_unsubscriber import EmailUnsubscriber


argParser = argparse.ArgumentParser(prog="Debug Scanned Emails", description="Allows a user to debug scanned emails, for internal use")
argParser.add_argument("-l", "--linked_email", help="the linked email to test on", required=True)

args = argParser.parse_args()

linked_email = args.linked_email

class MockTask:
    """A mock task class to simulate updating the celery state object
    """

    def __init__(self) -> None:
        self.state = 'PROGRESS'
        self.meta = {}

    def update_state(self, state, meta) -> None:
        self.state = state
        self.meta = meta

task = MockTask()


db = SessionLocal()

try:

    # Get the linked_email from the db
    linked_email_obj = (
        db.query(LinkedEmails)
        .filter(
            LinkedEmails.email == linked_email,
        )
        .first()
    )

    if not linked_email_obj:
        raise Exception(f"Could not find linked email {linked_email}")
    
    domain = EmailUnsubscriber.get_domain_from_email(
        email_address=linked_email_obj.email
    )
    email_unsubscriber = EmailUnsubscriber(email_type=domain)

    # Login the user and scan the emails.
    if not email_unsubscriber.login(
        email_username=linked_email_obj.email,
        email_password=security.decrypt_email_password(linked_email_obj.password),
    ):
        raise Exception(
            f"Could not login for linked email '{linked_email_obj.email}'",
        )
    
    status, messages = email_unsubscriber.imap.select("INBOX", readonly=True)
    if status != "OK":
        raise Exception("Could not select INBOX")
    
    number_of_emails = int(messages[0])

    # Scan ALL emails.
    range_params = (number_of_emails, 0, -1)
    
    # Scan emails for spam
    # TODO: This script actually scans emails and adds them to the scanned_email/unsubscribe_links table.
    # Since this is for testing only we should optionally allow the user to delete that data at the end of
    # the running of this script.
    spam_emails_found = email_unsubscriber._do_scan_emails(
        task=task,
        range_params=range_params,
        db=db,
    )

finally:
    del email_unsubscriber
    db.close()
