from pathlib import Path
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import File
from app.services.file_processing_service import process_file


def process_file_background(file_id: str, local_path: Path):
    """
    Background task for processing uploaded files.
    Uses its own DB session (important).
    """
    db: Session = SessionLocal()

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
