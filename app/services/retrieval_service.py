from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.embedding_service import generate_embedding


def semantic_search(
    db: Session,
    project_id: str,
    query: str,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    sql = text("""
        SELECT fc.content
        FROM file_chunks fc
        JOIN files f ON f.id = fc.file_id
        WHERE f.project_id = :project_id
        ORDER BY fc.embedding <-> :embedding
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "project_id": project_id,
            "embedding": query_embedding,
            "limit": limit,
        },
    )

    return [row[0] for row in result]
