from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from app.database.base_class import Base


class InviteCodes(Base):
    """The invite_codes table. This table holds codes available for new users
    to register with. Once an invite code is used it becomes 'used' and can not
    be used to register another account. When an invite code is generated it can
    be only be used within a certain amount of time before it becomes expired.

    An invite code can only be generated through scripts/generate_invite_code.py

    TODO: When the app is ready to be released to the public remove this table.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True, index=True, nullable=False)
    used = Column(Boolean, default=False)
    expire_ts = Column(
        DateTime(timezone=True), nullable=False,
    )
    insert_ts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
