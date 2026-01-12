from pathlib import Path
from sqlalchemy.orm import Session

from app.rag.text_extractor import extract_text_from_pdf
from app.rag.chunker import chunk_text
from app.services.chunk_service import save_chunks
from app.db.models import File


def process_file(
    db: Session,
    file: File,
    local_path: Path,
):
    text = extract_text_from_pdf(local_path)
    chunks = chunk_text(text)

    save_chunks(
        db=db,
        file_id=file.id,
        chunks=chunks,
    )

    file.status = "processed"
    db.commit()
