---
name: manage-github-pull-requests
description: Manage GitHub pull requests using the gh CLI. Use when creating, editing, viewing, listing, or updating pull requests, or when the user asks to open, create, or update a PR.
---

# Manage GitHub Pull Requests with gh CLI

Use the `gh` command line tool for all GitHub pull request operations.

## Common Commands

| Action | Command |
|--------|---------|
| List PRs | `gh pr list` |
| List open PRs | `gh pr list --state open` |
| View PR | `gh pr view <number>` |
| Create PR | `gh pr create --title "..." --body "..."` |
| Edit PR | `gh pr edit <number> --title "..." --body "..."` |
| Close PR | `gh pr close <number>` |
| Merge PR | `gh pr merge <number>` |
| Update branch | `gh pr update-branch <number>` |

## PR Body Template

When creating or editing PRs, use this template for the body:

```markdown
## Summary

[1–3 bullet points describing what this PR does and why]

## Changes

[Brief list of the key files / components changed and why]

## Related issues

Closes #<issue-number>   ← remove if no related issue
```

## Creating PRs

**From stdin** (useful for multi-line body):

```bash
gh pr create --title "Title here" --body-file - << 'EOF'
## Summary

- Fix cache eviction bug when TTL expires

## Changes

- `atomic_lru/cache.py`: corrected eviction logic
- `tests/test_cache.py`: added regression test

## Related issues

Closes #42
EOF
```

**Inline body**:

```bash
gh pr create --title "Title" --body "## Summary

- Short description of what this PR does

## Changes

- List of key changes

## Related issues

Closes #42" --label "Type: Fixed"
```

**Autofill from commits**:

```bash
gh pr create --fill
```

**Draft PR**:

```bash
gh pr create --draft --title "WIP: Feature" --body "..."
```

## Updating PRs

**Edit title and body**:

```bash
gh pr edit <number> --title "New title" --body "New body"
```

**Edit body from file**:

```bash
gh pr edit <number> --body-file - << 'EOF'
Updated body content.
EOF
```

**Add or remove labels**:

```bash
gh pr edit <number> --add-label "Type: Fixed" --add-label "Priority: High"
gh pr edit <number> --remove-label "Type: Added"
```

**Update branch** (rebase/merge base into head):

```bash
gh pr update-branch <number>
```

## Listing and Filtering

```bash
# Open PRs
gh pr list --state open

# By author
gh pr list --author "@me"

# By label
gh pr list --label "Type: Fixed"

# Limit results
gh pr list --limit 20
```

## Standardized Labels (for PRs)

PRs share the same labels as issues (see AGENTS.md):

- `Type: Added`, `Type: Changed`, `Type: Removed`, `Type: Fixed`, `Type: Security`, `Type: Dependencies`, `Type: Documentation`
- `Priority: Critical`, `Priority: High`, `Priority: Medium`, `Priority: Low`

PRs MUSTN'T have multiple `Status: *` or `Priority: *` or `Type: *` labels at the same time.

## Linking to Issues

Reference issues in the PR body to auto-close on merge:

- `Fixes #123` or `Closes #123` — closes the issue when the PR is merged
- `Refs #123` — links without auto-closing
