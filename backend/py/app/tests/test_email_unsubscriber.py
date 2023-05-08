from app.objects.email_unsubscriber import EmailUnsubscriber
from app.tests.html_emails.basic_promo import basic_promo


class TestEmailUnsubscriber:
    """Test email unsubscriber class"""

    def test_get_unsubscribe_links_html(self) -> None:
        """Test getting unsubscribe links from html emails"""
        assert [
            "https://github.com/konsav/email-templates/"
        ] == EmailUnsubscriber._get_unsubscribe_links_from_html(body=basic_promo)
