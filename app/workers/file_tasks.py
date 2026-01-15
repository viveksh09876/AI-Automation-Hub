from pathlib import Path
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import File
from app.services.file_processing_service import process_file


def process_file_task(file_id: str, local_path_str: str):
    """
    RQ worker task.
    """
    db: Session = SessionLocal()
    local_path = Path(local_path_str)

    try:
        file = db.get(File, file_id)
        if not file:
            return

        file.status = "processing"
        db.commit()

        process_file(
            db=db,
            file=file,
            local_path=local_path,
        )

        file.status = "processed"
        db.commit()

    except Exception:
        if file:
            file.status = "failed"
            db.commit()
        raise

    finally:
        db.close()
