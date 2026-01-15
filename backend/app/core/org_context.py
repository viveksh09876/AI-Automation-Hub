from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.db.models import UserOrganization, Organization


def get_current_org(
    x_org_id: str = Header(..., alias="X-Org-Id"),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    membership = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == user.id,
            UserOrganization.organization_id == x_org_id,
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this organization",
        )

    org = db.get(Organization, x_org_id)

    return {
        "organization": org,
        "membership": membership,
        "role": membership.role,
    }
