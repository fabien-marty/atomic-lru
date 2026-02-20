---
id: TASK-7
title: 'Improvement: Several tests don''t call `close()` on Cache/Storage objects'
status: Triage
assignee: []
created_date: '2026-02-20 14:13'
updated_date: '2026-02-20 14:15'
labels:
  - Improvement
dependencies: []
references:
  - tests/test_cache.py
  - tests/test_storage.py
priority: low
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Multiple test functions in `tests/test_cache.py` and `tests/test_storage.py` create `Cache` or `Storage` instances (which spawn expiration threads) but never call `close()`. Since the expiration thread is a daemon thread, this doesn't cause test hangs, but it means background threads linger until garbage collection.

**Affected tests in `test_cache.py`:**
- `test_cache_basic`, `test_cache_miss`, `test_cache_overwrite`, `test_cache_ttl`, `test_cache_custom_serializer`, `test_cache_serialization_error`, `test_cache_deserialization_error`, `test_cache_complex_objects`, `test_cache_lru_behavior`, `test_cache_size_limit`, `test_cache_delete`, `test_cache_clean_expired`, `test_cache_default_serializer_pickle`, `test_cache_multiple_operations`, `test_cache_empty_values`, `test_cache_default_ttl_sentinel`

**Affected tests in `test_storage.py`:**
- `test_storage_expiration_manual`, `test_storage_too_many_items`, `test_storage_various`, `test_max_size_limit`, `test_overwrite_existing_key_size_tracking`

**Suggested fix:** Add `close()` calls at the end of each test, or use a pytest fixture that automatically closes after each test.
<!-- SECTION:DESCRIPTION:END -->
