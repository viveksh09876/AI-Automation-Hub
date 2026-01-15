import uuid
from sqlalchemy.orm import Session
from app.db.models import FileChunk


def save_chunks(
    db: Session,
    file_id: str,
    chunks: list[dict],
):
    for c in chunks:
        chunk = FileChunk(
            id=str(uuid.uuid4()),
            file_id=file_id,
            chunk_index=c["index"],
            content=c["content"],
        )
        db.add(chunk)

    db.commit()
