import uuid
from sqlalchemy.orm import Session

from app.db.models import Organization, UserOrganization, User


def create_organization(
    db: Session,
    user: User,
    name: str,
):
    org = Organization(
        id=str(uuid.uuid4()),
        name=name,
    )

    membership = UserOrganization(
        user_id=user.id,
        organization_id=org.id,
        role="owner",
    )

    db.add(org)
    db.add(membership)
    db.commit()

    return org
