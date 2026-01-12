def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
):
    words = text.split()
    chunks = []

    start = 0
    index = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(
            {
                "index": index,
                "content": " ".join(chunk_words),
            }
        )
        start = end - overlap
        index += 1

    return chunks
