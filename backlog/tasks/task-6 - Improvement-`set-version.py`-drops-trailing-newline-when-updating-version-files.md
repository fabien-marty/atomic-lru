---
id: TASK-6
title: >-
  Improvement: `set-version.py` drops trailing newline when updating version
  files
status: Triage
assignee: []
created_date: '2026-02-20 14:13'
updated_date: '2026-02-20 14:15'
labels:
  - Improvement
dependencies: []
references:
  - set-version.py
priority: low
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In `set-version.py`, the `update_version_in_file` function reads a file, processes lines, and writes them back using `"\n".join(lines)`. However, `str.splitlines()` strips trailing newlines, and `"\n".join()` doesn't add a trailing one. This means the output file will be missing its trailing newline.

**Location:** `set-version.py`, line 22

```python
with open(file, "w") as g:
    g.write("\n".join(lines))
```

**Impact:** The modified files (`pyproject.toml`, `atomic_lru/__init__.py`) will lack a trailing newline after the version is set. This can cause git to show "No newline at end of file" warnings and may trigger linting failures.

**Fix:** Change to `g.write("\n".join(lines) + "\n")`.
<!-- SECTION:DESCRIPTION:END -->
