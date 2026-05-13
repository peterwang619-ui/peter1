"""Token counting and context estimation for LLM models."""

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    """
    Count the number of tokens in a text string.

    Args:
        text: The input text to count tokens for.
        encoding: The tiktoken encoding name (default: cl100k_base for GPT-4/3.5).

    Returns:
        Number of tokens.

    Example:
        >>> count_tokens("Hello, world!")
        4
    """
    if TIKTOKEN_AVAILABLE:
        enc = tiktoken.get_encoding(encoding)
        return len(enc.encode(text))
    else:
        # Fallback: rough estimation (1 token ≈ 4 characters for English)
        return len(text) // 4


def estimate_context(file_path: str, encoding: str = "cl100k_base") -> dict:
    """
    Estimate token count and context usage for a file.

    Args:
        file_path: Path to the file to analyze.
        encoding: The tiktoken encoding name.

    Returns:
        Dict with token count, character count, and estimated context percentage.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}

    char_count = len(text)
    token_count = count_tokens(text, encoding)

    # Assume GPT-4 context window of 128k tokens
    context_pct = (token_count / 128000) * 100

    return {
        "file": file_path,
        "characters": char_count,
        "tokens": token_count,
        "encoding": encoding,
        "context_usage_pct": round(context_pct, 2),
    }
