from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.org_context import get_current_org
from app.core.dependencies import get_db
from app.services.data_source_service import create_data_source
from app.db.models import Project, DataSource

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.post("")
def create_data_source_api(
    payload: dict,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == payload["project_id"],
            Project.organization_id == context["organization"].id,
        )
        .first()
    )

    if not project:
        return {"error": "Invalid project"}

    ds = create_data_source(
        db=db,
        project_id=project.id,
        source_type=payload["type"],
        config=payload.get("config"),
    )

    return {
        "id": ds.id,
        "type": ds.type,
        "config": ds.config,
    }

@router.get("/{project_id}")
def list_data_sources(
    project_id: str,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    sources = (
        db.query(DataSource)
        .join(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == context["organization"].id,
        )
        .all()
    )

    return [
        {
            "id": s.id,
            "type": s.type,
            "config": s.config,
        }
        for s in sources
    ]
