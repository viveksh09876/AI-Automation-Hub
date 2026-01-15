from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.org_context import get_current_org
from app.core.dependencies import get_db
from app.services.project_service import create_project
from app.db.models import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("")
def create_project_api(
    payload: dict,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    project = create_project(
        db=db,
        organization_id=context["organization"].id,
        name=payload["name"],
        project_type=payload["type"],
    )

    return {
        "id": project.id,
        "name": project.name,
        "type": project.type,
    }

@router.get("")
def list_projects(
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    projects = (
        db.query(Project)
        .filter(Project.organization_id == context["organization"].id)
        .all()
    )

    return [
        {
            "id": p.id,
            "name": p.name,
            "type": p.type,
        }
        for p in projects
    ]