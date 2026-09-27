import os
import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("EMBEDDING_MODEL", "bge-small-en-v1.5")

async def embed(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(f"{OLLAMA_BASE_URL}/api/embed", json={"model": MODEL, "input": text})
        response.raise_for_status()
        data = response.json()
        return data["embeddings"][0]
