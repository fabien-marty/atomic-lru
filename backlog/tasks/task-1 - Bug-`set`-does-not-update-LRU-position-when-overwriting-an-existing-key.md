---
id: TASK-1
title: 'Bug: `set()` does not update LRU position when overwriting an existing key'
status: Triage
assignee: []
created_date: '2026-02-20 14:13'
updated_date: '2026-02-20 14:15'
labels:
  - Bug
dependencies: []
references:
  - atomic_lru/_storage/storage.py
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In `atomic_lru/_storage/storage.py`, when `set()` overwrites an existing key, `OrderedDict.__setitem__` updates the value but does **not** move the key to the end of the order. This means the overwritten key retains its original LRU position instead of becoming the most recently used item.

**Location:** `atomic_lru/_storage/storage.py`, line 306

```python
# Store the value (moves to end of OrderedDict for LRU)
self._data[key] = value_obj
```

The comment says "moves to end of OrderedDict for LRU" but `OrderedDict.__setitem__` only puts new keys at the end — existing keys keep their position. This is a known `OrderedDict` behavior (unlike regular dict).

**Impact:** An item that is actively being updated via `set()` could be evicted before truly inactive items, violating LRU semantics.

**Fix:** After `self._data[key] = value_obj`, add `self._data.move_to_end(key)` (at least for the overwrite case). The docstring at line 235 already promises this behavior: "The item is moved to the end of the LRU order (most recently used)."

**No existing test covers this** — all LRU tests use `get()` to refresh positions, never `set()` overwrites.
<!-- SECTION:DESCRIPTION:END -->
