from pathlib import Path
from sqlalchemy.orm import Session

from app.rag.text_extractor import extract_text_from_pdf
from app.rag.chunker import chunk_text
from app.services.chunk_service import save_chunks
from app.db.models import File
from app.services.chunk_embedding_service import embed_chunks_for_file
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def process_file(
    db: Session,
    file: File,
    local_path: Path,
):
    text = extract_text_from_pdf(local_path)
    chunks = chunk_text(text)

    save_chunks(db=db, file_id=file.id, chunks=chunks)

    embed_chunks_for_file(db=db, file_id=file.id)

    file.status = "processed"
    db.commit()


def process_file_background(file_id: str, local_path: Path):
    """
    Runs in background task.
    Creates its own DB session.
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

    except Exception as e:
        file.status = "failed"
        db.commit()
        raise e

    finally:
        db.close()

