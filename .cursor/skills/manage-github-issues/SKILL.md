---
name: manage-github-issues
description: Manage GitHub issues using the gh CLI. Use when listing, creating, editing, viewing, or closing issues, or when the user asks to create or manage GitHub issues.
---

# Manage GitHub Issues with gh CLI

Use the `gh` command line tool for all GitHub issue operations. When creating issues as an AI agent, always add the `Reporter: AI` label.

## Common Commands

| Action | Command |
|--------|---------|
| List issues | `gh issue list` |
| List open issues | `gh issue list --state open` |
| View issue | `gh issue view <number>` |
| Create issue | `gh issue create --title "..." --body "..." --label "Reporter: AI"` |
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

## Label Management

Before creating issues, ensure all required standardized labels exist in the repository.

**Check existing labels:**

```bash
gh label list --limit 100
```

**Create a missing label** (use these exact names, colors, and descriptions):

```bash
# Type labels
gh label create "Type: Added"         --color "0075ca" --description "New feature"
gh label create "Type: Changed"       --color "e4e669" --description "Change to an existing feature"
gh label create "Type: Removed"       --color "e4e669" --description "Removal of an existing feature"
gh label create "Type: Fixed"         --color "d73a4a" --description "Bug fix"
gh label create "Type: Security"      --color "ee0701" --description "Security issue"
gh label create "Type: Dependencies"  --color "0075ca" --description "Dependency update"
gh label create "Type: Documentation" --color "0075ca" --description "Documentation change"

# Priority labels
gh label create "Priority: Critical"  --color "ee0701" --description "Critical priority"
gh label create "Priority: High"      --color "e4181b" --description "High priority"
gh label create "Priority: Medium"    --color "fbca04" --description "Medium priority"
gh label create "Priority: Low"       --color "c5def5" --description "Low priority"

# Reporter / workflow labels
gh label create "Reporter: AI"        --color "d4c5f9" --description "Created by AI agent"
gh label create "Human"               --color "fbca04" --description "Requires human intervention"

# Status labels
gh label create "Status: Validated"   --color "99d708" --description "Validated and ready to plan/implement"
gh label create "Status: Planning"    --color "0075ca" --description "Being planned"
gh label create "Status: Planned"     --color "0e8a16" --description "Plan validated"
gh label create "Status: Implementing" --color "0052cc" --description "Being implemented"
gh label create "Status: Implemented"  --color "0e8a16" --description "Implementation complete"
```

> **Important**: always run `gh label list` first and only create labels that are missing. Do not re-create existing ones.

## Creating Issues

**Required**: Add the `Reporter: AI` label to every issue created by an AI agent.

**From stdin** (useful for multi-line body):

```bash
gh issue create --title "Title here" --body-file - --label "Reporter: AI" << 'EOF'
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

Notes." --label "Reporter: AI"
```

## Listing and Filtering

```bash
# Open issues
gh issue list --state open

# By label
gh issue list --label "Reporter: AI"

# Limit results
gh issue list --limit 20
```

## Standardized labels

We use the following standardized labels:

- `Reporter: AI` - Issues created by AI agents
- `Human` - Issues that require human intervention (AI agents should skip these)

- `Status: Validated` - Issues that have been validated and that are ready to be planned/implemented
- `Status: Planning` - Issues that are being worked on in planning mode
- `Status: Planned` - Issues with a validated plan
- `Status: Implementing` - Issues that are being implemented
- `Status: Implemented` - Issues that have been implemented (in a pull-request or in a local branch)

- `Type: Added` - Issues that are new features
- `Type: Changed` - Issues that are changes to existing features
- `Type: Removed` - Issues that are removals of existing features
- `Type: Fixed` - Issues that are bug fixes
- `Type: Security` - Issues that are security issues
- `Type: Dependencies` - Issues that are dependencies changes
- `Type: Documentation` - Issues that are documentation changes

- `Priority: Critical`
- `Priority: High`
- `Priority: Medium`
- `Priority: Low`

Issues MUSTN'T have multiple `Status: *` or `Priority: *` or `Type: *` labels at the same time.
