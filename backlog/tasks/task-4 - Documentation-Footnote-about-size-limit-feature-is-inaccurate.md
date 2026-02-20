---
id: TASK-4
title: 'Documentation: Footnote about size limit feature is inaccurate'
status: Triage
assignee: []
created_date: '2026-02-20 14:13'
updated_date: '2026-02-20 14:15'
labels:
  - Documentation
dependencies: []
references:
  - docs/_includes/footnotes.md
  - docs/_includes/features.md
priority: low
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In `docs/_includes/footnotes.md`, footnote [^1] says:

> This feature is only available when using the high level `Cache` API.

This refers to "Total size limit (in bytes)" in the features list. However, `Storage[bytes]` also fully supports `size_limit_in_bytes` — it's defined in the `Storage` class, not `Cache`. The `Cache` class just ensures values are serialized to bytes, which makes size tracking work automatically.

The footnote is misleading because it implies `Storage` cannot use size limits at all, when in reality `Storage[bytes]` works perfectly with this feature.

**Suggested fix:** Rephrase to something like: "This feature requires storing `bytes` values. The high-level `Cache` API handles this automatically via serialization."
<!-- SECTION:DESCRIPTION:END -->
