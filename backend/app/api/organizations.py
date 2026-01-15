from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.services.organization_service import create_organization
from app.db.models import User
from app.db.models import UserOrganization
from app.core.org_context import get_current_org
from app.core.rbac import require_role

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("")
def create_org(
    payload: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    org = create_organization(
        db=db,
        user=user,
        name=payload["name"],
    )

    return {
        "id": org.id,
        "name": org.name,
    }

@router.get("")
def list_orgs(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    memberships = (
        db.query(UserOrganization)
        .filter(UserOrganization.user_id == user.id)
        .all()
    )

    return [
        {
            "id": m.organization.id,
            "name": m.organization.name,
            "role": m.role
        }
        for m in memberships
    ]

@router.delete("/{org_id}")
def delete_org(
    context=Depends(get_current_org),
    _: dict = Depends(require_role("owner")),
):
    org = context["organization"]

    return {
        "message": f"Organization {org.name} deleted (mock)",
    }

@router.get("/current")
def get_current_org_info(
    context=Depends(get_current_org),
):
    org = context["organization"]

    return {
        "id": org.id,
        "name": org.name,
        "role": context["role"],
    }