import uuid
from sqlalchemy.orm import Session
from app.db.models import DataSource


def create_data_source(
    db: Session,
    project_id: str,
    source_type: str,
    config: dict | None = None,
):
    ds = DataSource(
        id=str(uuid.uuid4()),
        project_id=project_id,
        type=source_type,
        config=config or {},
    )

    db.add(ds)
    db.commit()
    db.refresh(ds)

    return ds
