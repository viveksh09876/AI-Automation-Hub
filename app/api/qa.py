from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.org_context import get_current_org
from app.core.dependencies import get_db
from app.services.qa_service import answer_question

router = APIRouter(prefix="/qa", tags=["RAG"])


@router.post("/{project_id}")
def ask_question(
    project_id: str,
    payload: dict,
    context=Depends(get_current_org),
    db: Session = Depends(get_db),
):
    question = payload.get("question")

    if not question:
        return {"error": "Question is required"}

    result = answer_question(
        db=db,
        project_id=project_id,
        question=question,
    )

    return result
