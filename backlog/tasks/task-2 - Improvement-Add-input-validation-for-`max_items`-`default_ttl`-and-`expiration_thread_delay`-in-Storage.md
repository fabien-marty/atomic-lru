---
id: TASK-2
title: >-
  Improvement: Add input validation for `max_items`, `default_ttl`, and
  `expiration_thread_delay` in Storage
status: Triage
assignee: []
created_date: '2026-02-20 14:13'
updated_date: '2026-02-20 14:15'
labels:
  - Improvement
dependencies: []
references:
  - atomic_lru/_storage/storage.py
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
`Storage.__post_init__` validates `size_limit_in_bytes` but does not validate several other constructor parameters:

1. **`max_items`** — No validation. Setting `max_items=0` means no items can ever be stored (silently); `max_items=-1` would cause incorrect behavior in the eviction loop.
2. **`default_ttl`** — No validation. A negative value would be accepted at the `Storage` level but would later raise `ValueError` in `Value.__post_init__` when `set()` is called. Better to fail early.
3. **`expiration_thread_delay`** — No validation. A negative or zero value could cause the expiration thread to spin-loop consuming CPU.

**Location:** `atomic_lru/_storage/storage.py`, `__post_init__` method (line 100)

**Suggested fix:** Add validation for these parameters in `__post_init__`, before creating the expiration thread:
- `max_items`: must be > 0 if set
- `default_ttl`: must be >= 0 if set
- `expiration_thread_delay`: must be > 0
<!-- SECTION:DESCRIPTION:END -->
