---
id: TASK-5
title: >-
  Inconsistency: Import linter contract name `agents_embeddings` is a copy-paste
  artifact
status: Triage
assignee: []
created_date: '2026-02-20 14:13'
updated_date: '2026-02-20 14:15'
labels:
  - Inconsistency
dependencies: []
references:
  - .importlinter
priority: low
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In `.importlinter`, the contract is named `agents_embeddings`:

```ini
[importlinter:contract:agents_embeddings]
name = Use only exported symbols of atomic_lru._storage
```

The name `agents_embeddings` appears to be a copy-paste artifact from another project and doesn't describe the actual rule (which enforces that modules outside `_storage` only use the public exports of `atomic_lru._storage`).

**Suggested fix:** Rename the contract section to something descriptive, e.g., `[importlinter:contract:storage_encapsulation]`.
<!-- SECTION:DESCRIPTION:END -->
