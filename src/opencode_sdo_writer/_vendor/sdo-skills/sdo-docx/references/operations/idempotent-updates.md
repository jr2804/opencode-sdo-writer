# Idempotent updates

Avoid hanging paragraphs when scripts are re-run.

— avoid hanging paragraphs

When a script inserts paragraphs (figures, tables) that are later refreshed by
re-running the same script, **hanging paragraphs** accumulate — old inserted
elements are left behind and new ones are added on each run.

**Rules:**

- Before inserting Figure-style image paragraphs: query and remove ALL existing
  `style=Figure` paragraphs (exact match, not contains).
  - Use `paragraph[style=Figure]` — **not** `paragraph[style~=Figure]`.
  - Captions (`style=Figure_No & title` / `FigureNotitle0`) are
    updated **in-place** via `set`; do NOT remove them — they serve as stable
    anchor paraIds for the insertion `--before` target.
- Before rebuilding a table section: remove all dynamic tables by iterating
  `remove /body/tbl[N]` in a `while True / except RuntimeError: break` loop
  rather than a fixed count. A fixed count fails on repeated runs once tables
  have already been removed.
- Before removing paragraphs by paraId: wrap each removal in try/except
  (or check existence first) so the script is safe to run multiple times.
  ParaIds that were already removed on a previous run must not abort the script.
- **Exact vs contains style match matters:**
  - `paragraph[style=Figure]` — exact match (image containers only)
  - `paragraph[style~=Figure_No]` — contains match (would also remove captions)
