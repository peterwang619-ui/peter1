# TokScale

Token scaling and estimation tool for LLM context management.

## Features

- Count tokens in text or files using tiktoken encodings
- Estimate context window usage for files
- CLI and Python API
- Supports multiple token encodings (cl100k_base, p50k_base, etc.)

## Installation

```bash
pip install tokscale
```

Or install from source:

```bash
git clone https://github.com/peterwang619-ui/peter1.git
cd peter1
pip install -e .
```

## Usage

### CLI

```bash
# Count tokens in a text string
tokscale count "Hello, world!"

# Count tokens in a file
tokscale count file.txt

# Use a specific encoding
tokscale count file.txt --encoding p50k_base

# Estimate context usage for a file
tokscale estimate large_file.py
```

### Python API

```python
from tokscale import count_tokens, estimate_context

# Count tokens
count = count_tokens("Hello, world!")
print(f"Tokens: {count}")

# Estimate context usage
result = estimate_context("file.py")
print(result)
```

## Supported Encodings

- `cl100k_base` — GPT-4, GPT-3.5-turbo
- `p50k_base` — GPT-3 models
- `r50k_base` — Codex models

## Requirements

- Python >= 3.8
- tiktoken >= 0.5.0

## License

MIT
