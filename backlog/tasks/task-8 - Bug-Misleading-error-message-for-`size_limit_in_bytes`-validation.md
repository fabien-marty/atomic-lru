---
id: TASK-8
title: 'Bug: Misleading error message for `size_limit_in_bytes` validation'
status: In Progress
assignee: []
created_date: '2026-02-20 14:14'
updated_date: '2026-02-20 14:30'
labels:
  - Bug
  - Planned
  - Implemented
dependencies: []
references:
  - atomic_lru/_storage/storage.py
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In `atomic_lru/_storage/storage.py`, line 102-103:

```python
if self.size_limit_in_bytes is not None and self.size_limit_in_bytes < 4096:
    raise ValueError("size_limit_in_bytes must be greater than 4096")
```

The condition is `< 4096`, meaning 4096 itself is a valid value. But the error message says "must be greater than 4096", implying 4096 is invalid.

**Fix:** Change the error message to "size_limit_in_bytes must be at least 4096" (or "must be >= 4096").
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Fixed the misleading error message in `atomic_lru/_storage/storage.py` line 103.\n\nChanged:\n```\nraise ValueError(\"size_limit_in_bytes must be greater than 4096\")\n```\nTo:\n```\nraise ValueError(\"size_limit_in_bytes must be at least 4096\")\n```\n\nThe condition `< 4096` correctly allows 4096 as a valid value, so the message now accurately reflects this by saying \"at least 4096\" instead of \"greater than 4096\".\n\nAll linting, tests (30/30), and documentation generation pass.
<!-- SECTION:NOTES:END -->
