from fastapi import APIRouter, Depends, UploadFile, File as UploadFileType, HTTPException
from sqlalchemy.orm import Session
from app.core.org_context import get_current_org
from app.core.dependencies import get_db
from app.db.models import Project, File
from app.services.file_service import create_file_record, store_file
from app.services.storage_service import get_signed_download_url, delete_file_from_storage

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/{project_id}")
def upload_file(
    project_id: str,
    uploaded_file: UploadFile = UploadFileType(...),
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == context["organization"].id,
        )
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Invalid project")

    file_record = create_file_record(
        db=db,
        project_id=project.id,
        filename=uploaded_file.filename,
        mime_type=uploaded_file.content_type,
        size=None,
    )

    file_record = store_file(
        db=db,
        project_id=project.id,
        org_id=context["organization"].id,
        file_record=file_record,
        uploaded_file=uploaded_file,
    )

    return {
        "id": file_record.id,
        "filename": file_record.filename,
        "status": file_record.status,
        "storage_path": file_record.storage_path,
    }


@router.get("/{project_id}")
def list_files(
    project_id: str,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == context["organization"].id,
        )
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Invalid project")

    files = (
        db.query(File)
        .filter(File.project_id == project.id)
        .all()
    )

    return [
        {
            "id": f.id,
            "filename": f.filename,
            "status": f.status,
            "mime_type": f.mime_type,
            "size": f.size,
        }
        for f in files
    ]


@router.get("/download/{file_id}")
def download_file(
    file_id: str,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    file = (
        db.query(File)
        .join(Project)
        .filter(
            File.id == file_id,
            Project.organization_id == context["organization"].id,
        )
        .first()
    )

    if not file or not file.storage_path:
        raise HTTPException(status_code=404, detail="File not found")

    url = get_signed_download_url(
        bucket="project-files",
        path=file.storage_path,
    )

    return {"url": url}


@router.delete("/{file_id}")
def delete_file(
    file_id: str,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    file = (
        db.query(File)
        .join(Project)
        .filter(
            File.id == file_id,
            Project.organization_id == context["organization"].id,
        )
        .first()
    )

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.storage_path:
        delete_file_from_storage(
            bucket="project-files",
            path=file.storage_path,
        )

    db.delete(file)
    db.commit()

    return {"status": "deleted"}



