import uuid
from sqlalchemy.orm import Session
from app.db.models import WebhookEvent, DataSource, Project


def handle_webhook_event(
    db: Session,
    data_source_id: str,
    payload: dict,
):
    data_source = db.get(DataSource, data_source_id)
    if not data_source:
        return None

    project = db.get(Project, data_source.project_id)

    event = WebhookEvent(
        id=str(uuid.uuid4()),
        data_source_id=data_source.id,
        payload=payload,
        status="received",
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {
        "event_id": event.id,
        "project_id": project.id,
        "data_source_type": data_source.type,
        "payload": payload,
    }
