# TokScale & Hindsight & Mission Control & Hermes Workspace

Token scaling, retrospective analysis, task orchestration, and multi-project workspace management tools.

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

### Mission Control
- Task creation, tracking, and lifecycle management
- Task status management (pending, running, completed, failed, cancelled)
- CLI and Python API
- JSON-based persistent storage
- Extensible scheduler for task automation

### Hermes Workspace
- Multi-project workspace management
- Add, remove, list, and switch between projects
- JSON-based configuration
- CLI and Python API
- Persistent workspace state

### Stack
- Go project stack management
- Initialize, build, run, and deploy Go projects
- Manage multiple Go project stacks
- CLI and Python API
- JSON-based configuration

### Awesome Hermes
- Curated collection of Hermes Agent skills
- Search, list, and recommend skills
- Categorized skill directory
- CLI and Python API
- Skill installation tracking

## Installation

```bash
pip install toolscale
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

### Mission Control CLI

```bash
# List all tasks
mission-control list

# Create a new task
mission-control create "Deploy service" --description "Deploy to production"

# Check task status
mission-control status <task-id>

# Mark task as completed
mission-control complete <task-id>

# Cancel a task
mission-control cancel <task-id>

# Delete a task
mission-control delete <task-id>
```

### Hermes Workspace CLI

```bash
# List all projects
hermes-workspace list

# Add a new project
hermes-workspace add myproject /path/to/myproject --description "My awesome project"

# Switch to a project
hermes-workspace switch myproject

# Show current project
hermes-workspace current

# Remove a project
hermes-workspace remove myproject
```

### Stack CLI

```bash
# List all Go projects
stack list

# Initialize a new Go project
stack init myproject /path/to/myproject --module github.com/user/myproject

# Build a project
stack build myproject

# Run a project
stack run myproject --args "arg1 arg2"

# Remove a project
stack remove myproject
```

### Awesome Hermes CLI

```bash
# List all skills
awesome-hermes list

# Search skills
awesome-hermes search "python"

# Show skill details
awesome-hermes show repomix

# Recommend skills
awesome-hermes recommend "I need to manage tasks"

# Mark skill as installed
awesome-hermes mark-installed stack /tmp/peter1/stack
```

### Python API

```python
from tokscale import count_tokens, estimate_context
from hindsight import search_sessions, save_memory, load_memory
from mission_control import TaskManager, TaskStatus
from hermes_workspace import WorkspaceManager

# TokScale
count = count_tokens("Hello, world!")
print(f"Tokens: {count}")

# Hindsight
sessions = search_sessions("python")
save_memory("favorite_lang", "python")
value = load_memory("favorite_lang")

# Mission Control
manager = TaskManager()
task = manager.create_task("My Task", "Description here")
print(f"Created task: {task.id}")
manager.complete_task(task.id)

# Hermes Workspace
wm = WorkspaceManager()
wm.add_project("myproject", "/path/to/myproject")
wm.switch_project("myproject")
current = wm.get_current_project()

# Stack
sm = StackManager()
project = sm.init_project("myproject", "/path/to/myproject", "github.com/user/myproject")
result = sm.build_project("myproject")

# Awesome Hermes
catalog = SkillCatalog()
skills = catalog.search("python")
recommendations = catalog.recommend("I need to manage tasks")
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
