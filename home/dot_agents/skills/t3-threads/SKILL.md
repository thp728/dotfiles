---
name: t3-threads
description: How the user's work is split across T3 Code threads, covering coordinator and worker threads, subagents and delegates, decision rounds, settling, messages between threads, scheduled tasks, and work that spans both vaults. Use when T3's thread tools are present, before launching, messaging or settling a thread, delegating, or scheduling a task.
---

# T3 threads

This is how the user runs work across T3 Code threads. Where a thread's own brief differs, the brief wins.

## Coordinators and workers

- A **coordinator** thread owns an effort that spans several threads: its plan or roadmap, its task list, and every push. Each **worker** thread owns one piece of it, such as a folder, a review or a workstream. A worker commits only its own paths and never pushes.
- A worker finishes by sending its coordinator a `t3_thread_send` message with the commit SHAs, what changed, and what's still open. The coordinator asks the user before every push.
- **Cross-thread sync**: when your change reaches a folder or file that another thread owns, message that thread after your commit, even if it's settled. List the commits, files, moves and new rules. Name any uncommitted files it must leave unstaged, and ask it to update its part. If no thread owns the affected part, say so in your final report.
- Act on other threads only as far as the work needs: settle, archive, rename or message one only when the work calls for it. A coordinator stays unsettled until the user says otherwise.
- **Settling** (`t3_thread_organize`, action `settle`) marks a thread as finished and takes it off the active list. Its history stays, and a new message reopens it. Settle a thread once its work is done and reported, and only if you own it or were asked to.
- A new top-level thread is for substantial work the user asked to start. Its brief must stand on its own: the goal, the files it owns, decisions already made, the rules it follows, and who it reports to.

## Subagents and delegates

- Hand read-only fact-finding across several files to a subagent, so this thread keeps the conclusion without the file dumps.
- Web research and independent audits go to a Codex delegate: `delegate_task` with provider `codex`, model `gpt-6.1-sol`, `reasoningEffort: "high"` and `runtimeMode: "auto"`. Always pass `auto`: Codex fails to start in full access.
- **Fanout** means two or more subagents or delegates running at once. Explain the tradeoff and wait for the user's yes, unless a skill they invoked calls for it. A single background subagent while you keep working doesn't count as fanout.

## Decision rounds

Bring consequential choices to the user in numbered rounds. Each question carries the background and options it needs:

> ❓ **Q1.** The question.
> ➡️ Your recommendation, and why.

The user replies by quoting each question with a comment. Apply only what they approve, then record the round where the repo's instructions say decisions go.

## Work across both vaults

The global `AGENTS.md` names the personal vault, Life OS, and the work vault. A thread that reads and writes both runs as one thread, in the project of the vault that takes most of the writes. Before writing to a vault, read its `AGENTS.md`. Its rules govern that write:

- In Life OS, every commit goes through its vault check and names its paths.
- The work vault syncs through OneDrive and has no Git. List the exact paths for the user's yes before any move, rename or delete.
- Work content stays out of Life OS's Git. Only lines screened under Life OS's ownership rule cross over.

List each batch's paths by vault. Use two threads that message each other only when each side is large enough to stand alone.

## Scheduled tasks

- Work routines run in the Work Vault project: the morning brief, start the day, the public-profile harvest and the work weekly review. Personal routines, such as the Media digest's, run in the Personal Vault project. Machine and T3 housekeeping runs in the Personal Dotfiles project.
- Bind each routine family to a single thread, and run it on Claude. Cursor stops when the organisation hits its monthly limit.
- Each task's source file lives in the dotfiles repo that its paths belong to. The `dotfiles` skill covers `t3-schedules`.

## Inbox

The pinned Inbox thread, in "No project", routes whatever the user drops into it. Its rules are in the `inbox` skill.
