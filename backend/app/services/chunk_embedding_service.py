from sqlalchemy.orm import Session
from app.db.models import FileChunk
from app.services.embedding_service import generate_embedding


def embed_chunks_for_file(db: Session, file_id: str):
    chunks = (
        db.query(FileChunk)
        .filter(
            FileChunk.file_id == file_id,
            FileChunk.embedding == None,
        )
        .all()
    )

    for chunk in chunks:
        chunk.embedding = generate_embedding(chunk.content)

    db.commit()
