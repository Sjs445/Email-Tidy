"""add cascades

Revision ID: 5c2831f87aff
Revises: 21627028bc87
Create Date: 2023-03-18 21:48:52.315969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5c2831f87aff"
down_revision = "21627028bc87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "linked_emails", "user_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_constraint(
        "linked_emails_user_id_fkey", "linked_emails", type_="foreignkey"
    )
    op.create_foreign_key(
        "linked_emails_user_id_fkey",
        "linked_emails",
        "users",
        ["user_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "scanned_emails_linked_email_address_fkey", "scanned_emails", type_="foreignkey"
    )
    op.create_foreign_key(
        "scanned_emails_linked_email_address_fkey",
        "scanned_emails",
        "linked_emails",
        ["linked_email_address"],
        ["email"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "unsubscribe_links_linked_email_address_fkey",
        "unsubscribe_links",
        type_="foreignkey",
    )
    op.drop_constraint(
        "unsubscribe_links_scanned_email_id_fkey",
        "unsubscribe_links",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "unsubscribe_links_scanned_email_id_fkey",
        "unsubscribe_links",
        "scanned_emails",
        ["scanned_email_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "unsubscribe_links_linked_email_address_fkey",
        "unsubscribe_links",
        "linked_emails",
        ["linked_email_address"],
        ["email"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###

    # manual commands for bytea type on linked_emails.password
    op.execute(
        "ALTER TABLE linked_emails ALTER COLUMN password type bytea USING password::bytea"
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "unsubscribe_links_scanned_email_id_fkey",
        "unsubscribe_links",
        type_="foreignkey",
    )
    op.drop_constraint(
        "unsubscribe_links_linked_email_address_fkey",
        "unsubscribe_links",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "unsubscribe_links_scanned_email_id_fkey",
        "unsubscribe_links",
        "scanned_emails",
        ["scanned_email_id"],
        ["id"],
    )
    op.create_foreign_key(
        "unsubscribe_links_linked_email_address_fkey",
        "unsubscribe_links",
        "linked_emails",
        ["linked_email_address"],
        ["email"],
    )
    op.drop_constraint(
        "scanned_emails_linked_email_address_fkey", "scanned_emails", type_="foreignkey"
    )
    op.create_foreign_key(
        "scanned_emails_linked_email_address_fkey",
        "scanned_emails",
        "linked_emails",
        ["linked_email_address"],
        ["email"],
    )
    op.drop_constraint(
        "linked_emails_user_id_fkey", "linked_emails", type_="foreignkey"
    )
    op.create_foreign_key(
        "linked_emails_user_id_fkey", "linked_emails", "users", ["user_id"], ["id"]
    )
    op.alter_column(
        "linked_emails", "user_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###

    # Manual commands for converting back password to text
    op.execute(
        "ALTER TABLE linked_emails ALTER COLUMN password type text USING password::text"
    )