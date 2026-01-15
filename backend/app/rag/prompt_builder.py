def build_rag_prompt(
    question: str,
    context_chunks: list[str],
) -> str:
    context = "\n\n".join(context_chunks)

    return f"""
You are an AI assistant answering questions using ONLY the provided context.

Rules:
- If the answer is not in the context, say "I don't know based on the provided documents."
- Do NOT use external knowledge.
- Be concise and factual.

Context:
{context}

Question:
{question}

Answer:
""".strip()
