import uuid
from sqlalchemy.orm import Session
from app.db.models import Project


def create_project(
    db: Session,
    organization_id: str,
    name: str,
    project_type: str,
):
    project = Project(
        id=str(uuid.uuid4()),
        organization_id=organization_id,
        name=name,
        type=project_type,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project
