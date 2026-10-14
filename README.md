# Coding Assistant

An experimental tool-using coding agent built with Python and LangChain. The model can request file-reading and shell-execution tools, receive their outputs, and continue its agent loop.

## Current capabilities

- Uses NVIDIA's hosted chat model through `ChatNVIDIA`.
- Exposes a `read_file` tool for reading workspace files.
- Exposes a `run_bash` tool that runs commands in a Docker container with networking disabled and a 30-second timeout.
- Limits the agent loop to 10 turns.

## Architecture

```text
User prompt
    ↓
Chat model with bound tools
    ↓
Agent loop ── tool request ──→ read_file / run_bash
    ↑                              ↓
    └──────── tool result ─────────┘
```

## Setup

Requirements: Python 3.13+, [uv](https://docs.astral.sh/uv/), Docker, and an NVIDIA API key.

```bash
git clone https://github.com/Dhairy4/coding_assistant.git
cd coding_assistant
uv sync
cp .env.example .env
```

Add your own key to `.env`:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

Run the current entry point:

```bash
uv run python main.py
```

Docker must be running and available to the user executing the agent.

## Important limitations

This is a learning prototype, not a production-ready autonomous coding environment. The Docker runner disables container networking, but it mounts the current working directory into the container; treat that workspace as writable by model-requested commands. Do not run it against sensitive files or untrusted tasks. The sandbox needs additional hardening before use with real repositories.

The current entry point contains a sample prompt. Add configuration and tests before treating the project as a reusable tool.

## Next steps

- Move prompts and model settings into explicit configuration.
- Add unit tests for tool calls, errors, timeouts, and turn-limit behavior.
- Restrict command execution with an allowlist and a dedicated temporary workspace.
- Add structured logs and clear final-answer handling.
