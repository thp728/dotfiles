---
name: inbox
description: Rules for the Inbox thread, which sorts whatever the user drops in and routes each item to the right vault, to Todoist, or to a new T3 thread. Use in the thread titled Inbox, or when asked to follow the inbox skill.
---

# Inbox

The Inbox thread is a triage desk. The user drops in notes, tasks, links and requests, and each item goes to its owner. Substantial work always starts in its own thread: this thread files items and launches threads, and leaves the work to them. The global `AGENTS.md` gives both vaults' paths.

## Each message

1. Split the message into items. One message can carry several items, and an item can be a link, a sentence or a pasted block.
2. Sort each item:
   - **Work** means the employer's products, systems, delivery, colleagues or work tooling. It goes to the work vault.
   - **Personal** means the user's own direction, career, health, money, interests, projects and learning. It goes to Life OS.
   - **Machine or T3**: dotfiles, T3 settings or schedules. This goes to the Personal Dotfiles project, or to Work Dotfiles if it names the employer (the `dotfiles` skill's rule).
   - **Code repo**: work on a codebase goes to that repo's T3 project.
   - **Unclear**: ask about it (step 5).
3. Route each item by size:
   - A **quick note** fits in a few lines and needs no decision. A work note becomes one line under `## Capture` in today's work daily note, with anything longer going to an `01-inbox/` file linked from that line, as the work vault's `03-areas/daily-notes/AGENTS.md` describes. A personal note becomes an agent capture in Life OS, as the Capture section of its `system/operating-guidelines.md` describes.
   - A **quick task**: a work task is a task line in today's work daily note. A personal task goes to Todoist through Life OS's Todoist tool, following its rules.
   - **Substantial work** is anything that needs research, a decision, edits beyond one note, or more than a few tool calls. Launch a thread for it with `t3_thread_launch` in the right project (`t3_project_list` finds it), titled after the work. Its brief must stand on its own: the user's words verbatim, the goal, any owner files you know of, and that the thread reports straight to the user.
4. Before writing to either vault, read its root `AGENTS.md` and follow its rules for that write. Keep the user's words as given, with the source beside them. In Life OS, each write is a commit of its own path through the vault check.
5. If the sort or the route is unclear, ask: one numbered question per item, with your best guess. Hold that item, unwritten, until the user answers. Route the rest of the message meanwhile.

Done when every item in the message has been filed, launched, or held behind a question.

## Reply

Give one line per item: what it was, then where it went (the file path, the Todoist task, or the new thread's `link`) or the question that holds it.
