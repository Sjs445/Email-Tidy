import re

from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically.
        Convert a class name like this 'LinkedEmails' into a table name
        like this 'linked_emails'. Lowercased and underscore separated.

        Returns:
            str: The table name.
        """
        table_name_list = re.findall("[A-Z][a-z]*", cls.__name__)
        return "_".join(table_name_list).lower()
