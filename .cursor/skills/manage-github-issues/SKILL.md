---
name: manage-github-issues
description: Manage GitHub issues using the gh CLI. Use when listing, creating, editing, viewing, or closing issues, or when the user asks to create or manage GitHub issues.
---

# Manage GitHub Issues with gh CLI

Use the `gh` command line tool for all GitHub issue operations. When creating issues as an AI agent, always add the `ai` label.

## Common Commands

| Action | Command |
|--------|---------|
| List issues | `gh issue list` |
| List open issues | `gh issue list --state open` |
| View issue | `gh issue view <number>` |
| Create issue | `gh issue create --title "..." --body "..." --label "ai"` |
| Edit issue | `gh issue edit <number> --title "..." --body "..."` |
| Close issue | `gh issue close <number>` |

## Issue Body Template

When creating or editing issues, use this template for the body:

```markdown
## Description

[Describe the issue, feature request, or task in 1–3 paragraphs.]

## Acceptance criteria

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Implementation plan / notes

[Optional: technical notes, suggested approach, or implementation hints.]
```

## Creating Issues

**Required**: Add the `ai` label to every issue created by an AI agent.

**From stdin** (useful for multi-line body):

```bash
gh issue create --title "Title here" --body-file - --label "ai" << 'EOF'
## Description

Description text.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Implementation plan / notes

Notes here.
EOF
```

**Inline body**:

```bash
gh issue create --title "Title" --body "## Description

Description text.

## Acceptance criteria

- [ ] Criterion 1

## Implementation plan / notes

Notes." --label "ai"
```

## Listing and Filtering

```bash
# Open issues
gh issue list --state open

# By label
gh issue list --label "ai"

# Limit results
gh issue list --limit 20
```
