# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base
from app.models.users import User
from app.models.linked_emails import LinkedEmails
from app.models.scanned_emails import ScannedEmails
from app.models.unsubscribe_links import UnsubscribeLinks
