from openai import OpenAI
from app.core.config import settings
from app.rag.prompt_builder import build_rag_prompt
from app.services.retrieval_service import semantic_search

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def answer_question(
    db,
    project_id: str,
    question: str,
):

    chunks = semantic_search(
        db=db,
        project_id=project_id,
        query=question,
        limit=5,
    )

    if not chunks:
        return {
            "answer": "I don't know based on the provided documents.",
            "sources": [],
        }

    prompt = build_rag_prompt(
        question=question,
        context_chunks=chunks,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "sources": chunks,
    }
