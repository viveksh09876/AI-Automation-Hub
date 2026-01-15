import uuid
from sqlalchemy.orm import Session
from app.db.models import File
from app.services.storage_service import upload_file_to_storage


def create_file_record(
    db: Session,
    project_id: str,
    filename: str,
    mime_type: str,
    size: int | None,
):
    file = File(
        id=str(uuid.uuid4()),
        project_id=project_id,
        filename=filename,
        mime_type=mime_type,
        size=size,
        status="uploaded",
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    return file

def store_file(
    db,
    project_id: str,
    org_id: str,
    file_record,
    uploaded_file,
):
    storage_path = (
        f"{org_id}/{project_id}/"
        f"{file_record.id}/{uploaded_file.filename}"
    )

    content = uploaded_file.file.read()

    upload_file_to_storage(
        bucket="project-files",
        path=storage_path,
        content=content,
        content_type=uploaded_file.content_type,
    )

    file_record.storage_path = storage_path
    db.commit()
    db.refresh(file_record)

    return file_record

