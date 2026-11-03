# learn-claude-code — Repository Summary

> Generated summary of `README.md` and `requirements.txt`.

## Core Thesis

**Agency comes from the model. An agent product = Model + Harness.**

- Intelligence (perceive / reason / act) is *learned in training*, not coded — DQN (2013), OpenAI Five (2019), AlphaStar (2019), Tencent Jueyu (2019), and modern LLM coding agents all follow the same pattern: a trained model placed in an environment with tools.
- What engineers actually build is the **harness** — the operational environment around the model. The model is the driver; the harness is the vehicle.
- Anti-pattern the repo rejects: drag-and-drop workflow builders and prompt-chain orchestration that try to *code* agency via if-else trees and node graphs.

## Harness Definition

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions

  Tools:        file I/O, shell, network, database, browser
  Knowledge:    docs, API specs, style guides (loaded on demand)
  Observation:  git diff, error logs, browser state, sensor data
  Action:       CLI commands, API calls, UI interactions
  Permissions:  sandboxing, approval workflows, trust boundaries
```

Harness engineers: implement tools, curate knowledge, manage context, control permissions, and collect trajectory data (training signal for future models).

## The Agent Pattern (the constant loop)

```
User --> messages[] --> LLM --> response
                                  |
                          tool_use block?
                       /                  \
                     yes                   no
                      |                     |
                execute tools          return text
                append results
                loop back --> messages[]
```

Minimal implementation:

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            return

        results = []
        for block in tool_calls:
            output = TOOL_HANDLERS[block.name](**block.input)
            results.append({"type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output})
        messages.append({"role": "user", "content": results})
```

**Claude Code decomposed** = one agent loop + tools (bash/read/write/edit/glob/grep/browser) + on-demand skill loading + context compaction + subagent spawning + task system + async mailbox teams + task-bound worktrees + permission governance + hooks + memory + MCP routing.

## Course Structure — 17 Lessons (current track)

Each chapter: `README.md` (English default) + `README.zh.md` + `README.ja.md` + `code.py` + `images/`.

| # | Topic | Key Concepts | Motto / Idea |
|---|-------|--------------|--------------|
| s01 | Agent Loop | `messages`, `while True`, `tool_use` | One loop + Bash is all you need |
| s02 | Tool Use | `TOOL_HANDLERS`, dispatch map, concurrency | Adding a tool = adding one handler |
| s03 | Permission System | `PermissionRule`, approval pipeline | Set boundaries first, then grant freedom |
| s04 | Hook System | `PreToolUse`, `PostToolUse` | Hook around the loop, never rewrite it |
| s05 | TodoWrite | `TodoItem`, plan-then-execute | An agent without a plan drifts |
| s06 | Subagent | fresh `messages[]`, context isolation | Subtask's final text returns as one tool result |
| s07 | Skill Loading | `SkillLoader`, catalog, on-demand injection | Load knowledge on demand, not upfront |
| s08 | Context Compact | tool_result_budget, snip/micro/compact_history | Context always fills up — make room |
| s09 | Memory System | selection, extraction, consolidation | Remember what matters, forget what doesn't |
| s10 | Task System | `TaskRecord`, `blockedBy`, disk persistence | Big goals → small ordered persisted tasks |
| s11 | Background Tasks | threaded execution, notification queue | Slow ops go background, agent keeps thinking |
| s12 | Cron Scheduler | durable scheduling, session-scoped triggers | Fire on schedule, no human kick needed |
| s13 | Agent Teams | teammates, atomic task claims, worktrees, typed protocols | Too big for one agent — divide the work |
| s14 | MCP Plugin | tool discovery, namespaced tools, tool pool | Not enough capability? Plug in via MCP |
| s15 | Integrated Harness | all mechanisms around one loop | Many mechanisms, one loop |
| s16 | Workflow Runtime | script orchestration, lifecycle events, journal resume | Fixed orchestration shapes belong in code |
| s17 | Goal Loop | goal gate, conversation evaluation, auto-continuation | A goal decides when the loop may stop |

**Learning path:** act → handle complex work → remember across sessions → run long tasks → collaborate → extend & assemble → orchestrate & close goals.

## Two Tracks

- **Current:** root-level `s01_*` … `s17_*` — canonical, 17 lessons.
- **Legacy:** `docs/` and `agents/` — older 12-lesson version kept for old links (`s01`–`s12` + `s_full.py`).
- Chapter numbers do **not** always align across tracks (e.g. legacy s03 → new s05; legacy s04 → new s06). Don't mix numbering.

## Quick Start

```sh
git clone https://github.com/shareAI-lab/learn-claude-code
cd learn-claude-code
pip install -r requirements.txt
cp .env.example .env   # configure ANTHROPIC_API_KEY

python s01_agent_loop/code.py        # start here
python s08_context_compact/code.py   # context compaction (complex)
python s17_goal_loop/code.py         # endpoint: continue until goal is met
```

Legacy: `python agents/s01_agent_loop.py`, `python agents/s_full.py`
Web app: `cd web && npm install && npm run dev` → http://localhost:3000

## Dependencies (`requirements.txt`)

| Package | Constraint | Purpose |
|---------|------------|---------|
| `anthropic` | `>=0.25.0` | Claude API client (`client.messages.create`, tool_use blocks) |
| `python-dotenv` | `>=1.0.0` | Load `ANTHROPIC_API_KEY` from `.env` |
| `pyyaml` | `>=6.0` | Parse skill / config YAML files (e.g. s07 skill loading) |

Python project, no pinned lockfile — only three runtime deps, keeping each chapter standalone. Tests live in `tests/` (pytest suite covering chapters, runtime boundaries, and encoding).

## Repository Layout

```
learn-claude-code/
  s01_agent_loop/ ... s17_goal_loop/   # 17 chapters (README en/zh/ja + code.py + images)
  agents/                              # legacy 12 runnable copies + s_full.py
  skills/                              # skill files used by s07
  docs/                                # legacy 12-lesson docs (transitional)
  web/                                 # generated web course
  tests/                               # pytest suite
  requirements.txt
```

## What's Next (per README)

- **Kode Agent CLI** — `npm i -g @shareai-lab/kode`; skill + LSP support, Windows compatible, works with GLM / MiniMax / DeepSeek.
- **Kode Agent SDK** — embed agent capabilities without per-user process overhead.

**Sister repo [claw0](https://github.com/shareAI-lab/claw0)** — always-on harness: `agent core + heartbeat + cron + IM chat + memory + soul`. Where learn-claude-code covers use-and-discard sessions, claw0 covers a self-waking assistant (heartbeat every 30s, self-scheduled cron, multi-channel IM, Soul personality).

## Key Takeaways

1. You cannot engineer agency into existence — you engineer the environment it acts in.
2. Keep the loop constant; mechanisms (tools, knowledge, permissions) change.
3. Load context on demand — skills, subagents, compaction all serve this.
4. Persist beyond the conversation — tasks, memory, journals, cron.
5. Permission and evaluation gates (s03, s17) give freedom its safety rails.
6. "This is not 'copy the source code.' This is 'grasp the key designs and build it yourself.'"

License: MIT
