# Study Loop

A self-evolving tutor harness with a single chat as its whole interface. Tell it what you want to learn (a topic, a paper, a blog post, a LeetCode problem, or a whole reading list). It picks a teaching method for that kind of material, teaches one thing at a time, and rewrites its own teaching playbook from your results.

Live version: https://claude.ai/artifact/CVH22iCNV3JHg84zQzCX3m

## What it does

- **Spawned workspaces.** Give it one thing or a list. It writes a straight-shot plan (milestones from zero to mastery, each with a testable goal) and has Claude build a custom interactive workspace for that subject: explorables, step-throughs, guess-then-reveal prompts, code labs, one stage per milestone, each ending in a mastery check. The workspace runs in a sandboxed iframe and talks to the app through `window.SL`: `run(code, tests, viz)` (Python runner), `ask(prompt)` (Claude), `fig(n)` (source figures), `progress(milestone, score, note)` and `save/state` (resume). Mastery scores feed spaced reviews and the playbook. Say "rebuild the workspace with …" to change it.

- **Teacher chat.** Plain language does everything: "teach me DPO", a paper link, "too easy", "more visual", "skip", "what am I learning?", "show my list". A router decides the action: learn, next, skip, switch format, feedback, progress, read, focus, delete, library, cluster, organize, help or chat.
- **Method per kind of material.**
  - ML coding: deliberate practice against tests.
  - Papers: a PyTorch build (from research-implementation-engine) plus diagrams.
  - Blogs: figures, explaining it back, quizzes.
  - Interviews: timed mock and design rounds scored on correctness, reasoning, testing, performance and communication.
  - Facts: flashcards with spaced repetition.
- **Code workspace.** CodeMirror editor; tests rerun in the background (Pyodide in a Web Worker) about a second after you stop typing. Results show as a pass/fail list with errors and timings. Infinite loops are killed and the runner restarts.
- **Verified tests.** Each code exercise comes with a hidden reference solution. The tests are run against it first; tests that disagree are repaired or dropped before you see them.
- **Research.** Papers come in through alphaXiv (full text), and the official GitHub repo is read to ground signatures and tests. Known problems use their canonical examples and the edge cases people commonly fail.
- **Watches you work.** 3 fails in a row on the same test gives you a hint. All tests passing triggers an automatic interview-style review. Revealing the solution caps that exercise's score at 50.
- **Full blog capture.** `bookmarklet.js` runs on the post in your own browser and captures text, images (as data URIs), inline SVG diagrams and KaTeX/MathJax as TeX. Paste the capture into the chat: images are stored as assets, and Claude sees the figures when writing exercises.
- **Library import.** Paste a list or drop a file (bookmarks HTML or JSON, markdown, CSV, plain links). In the background it identifies each item, groups them into ordered clusters, marks overlaps (with which to use as primary), duplicates, and items your existing tracks already cover. Each cluster becomes one track with "Learn this cluster".
- **Self-evolving.** Spaced repetition (SM-2-style intervals), style votes, and a learner model. A per-kind **teaching playbook** is rewritten from scores, how well things stuck on review, time spent and your explicit requests, every 3 sessions at first and every 5 later. The teacher tells you when it changes something.

## Files

| File | What |
|---|---|
| `index.html` | The whole app: one self-contained page (UI, router, scheduler, runner, worker source, Python harness) |
| `capabilities.json` | Capabilities the page declares on the Claude artifact runtime |
| `bookmarklet.js` | Readable source of the "Send to Study Loop" bookmark (the page installs it for you) |
| `test_harness.py` | Readable copy of the Python test harness embedded in `index.html` |

## Runtime

It runs as a Claude artifact and uses `window.claude.use(...)`:

- `sample`: calls Claude for planning, exercises, grading, routing and playbook updates (with images)
- `db` + `user`: per-user private storage (`data/users/<id>/`: `profile`, `library`, `t_<trackId>`)
- `assets`: captured blog images and article HTML
- `downloads`: Colab notebook export
- `mcp`: alphaXiv `get_paper_content` and `read_files_from_github_repository`

Opened outside Claude (e.g. GitHub Pages), it only saves progress in that browser and the tutor stays off.

CDN libraries: Pyodide 0.26.4 (jsDelivr), CodeMirror 5.65.16 (cdnjs; base CSS inlined, MIT), Mermaid 10.9.1 (jsDelivr).

## Known limits

- PyTorch doesn't run in the browser, so paper builds export to Colab and you paste the output back for review.
- The in-page tutor has no general web search. Research covers papers and official repos (alphaXiv) and Claude's own knowledge.
- Blog images hosted on another site that blocks copying may not come through; their captions are kept.
