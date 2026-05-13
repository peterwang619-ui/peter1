# TokScale & Hindsight

Token scaling, estimation, and retrospective analysis tools for LLM context management.

## Features

### TokScale
- Count tokens in text or files using tiktoken encodings
- Estimate context window usage
- CLI and Python API
- Supports multiple token encodings (cl100k_base, p50k_base, etc.)

### Hindsight
- Session search and retrospective analysis
- Cross-session memory management
- CLI and Python API
- Local JSON-based storage

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

### TokScale CLI

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

### Hindsight CLI

```bash
# List recent sessions
hindsight list

# Search sessions
hindsight search "python"

# Memory management
hindsight memory get mykey
hindsight memory set mykey myvalue
hindsight memory delete mykey
hindsight memory list
```

### Python API

```python
from tokscale import count_tokens, estimate_context
from hindsight import search_sessions, save_memory, load_memory

# TokScale
count = count_tokens("Hello, world!")
print(f"Tokens: {count}")

# Hindsight
sessions = search_sessions("python")
save_memory("favorite_lang", "python")
value = load_memory("favorite_lang")
```

## Supported Encodings (TokScale)

- `cl100k_base` — GPT-4, GPT-3.5-turbo
- `p50k_base` — GPT-3 models
- `r50k_base` — Codex models

## Requirements

- Python >= 3.8
- tiktoken >= 0.5.0

## License

MIT
