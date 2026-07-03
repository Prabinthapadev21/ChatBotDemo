"""
Shared Groq LLM client.

Keeping this in one place means the QA engine, and any future module that
needs an LLM call (e.g. query rewriting, relevance grading), all go through
the same client and config -- no scattered `Groq(api_key=...)` calls.
"""

from typing import Iterable, List, Optional

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_MAX_TOKENS, GROQ_TEMPERATURE

_client: Optional[Groq] = None


def get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file."
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def chat_completion(
    messages: List[dict],
    model: str = GROQ_MODEL,
    max_tokens: int = GROQ_MAX_TOKENS,
    temperature: float = GROQ_TEMPERATURE,
) -> str:
    """Non-streaming chat completion. `messages` follows the standard
    [{"role": "system"|"user"|"assistant", "content": "..."}] format."""
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content


def stream_chat_completion(
    messages: List[dict],
    model: str = GROQ_MODEL,
    max_tokens: int = GROQ_MAX_TOKENS,
    temperature: float = GROQ_TEMPERATURE,
) -> Iterable[str]:
    """Streaming chat completion. Yields text chunks as they arrive --
    used by the Streamlit UI for token-by-token rendering."""
    client = get_client()
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
