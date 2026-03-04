# Update an already-opened GitHub Pull Request for the current branch

## Overview

Analyse the current branch state, handle uncommitted changes, sync with the remote base branch (rebase), push, and update the open Pull Request (title + body) using the `gh` CLI.

## Steps

### 1. Gather context

Run the following in parallel:

- `git branch --show-current` — get the current branch name
- `git status --short` — detect untracked/modified/staged files
- `git remote get-url origin` — confirm the remote
- `gh pr view --json number,title,body,baseRefName` — fetch the existing PR metadata (number, current title/body, base branch)

If `gh pr view` returns an error (no open PR for this branch), stop and tell the user.

### 2. Handle uncommitted / untracked changes

#### Case A — working tree is clean
Nothing to do, proceed to step 3.

#### Case B — there are uncommitted changes (modified, staged, or untracked files)

- Run `make lint`, `make test`, `make doc` in sequence. Stop and report if any fails.
- Stage everything:
  ```bash
  git add -A
  ```
- Derive a short imperative commit message from the diff, then commit:
  ```bash
  git commit -m "<type>: <short description>"
  ```

### 3. Rebase on top of the remote base branch

Fetch the latest state of the remote, then rebase:

```bash
git fetch origin
git rebase origin/<base-branch>
```

Where `<base-branch>` is the value of `baseRefName` from step 1 (typically `main`).

#### If the rebase succeeds with no conflicts
Proceed to step 4.

#### If there are conflicts

- Inspect the conflicting files:
  ```bash
  git diff --name-only --diff-filter=U
  ```
- For each conflicting file, read the conflict markers and resolve them by keeping the appropriate content (prefer the incoming change when it is unambiguous, otherwise merge both sides logically). Use the file-edit tools to apply the resolution directly.
- After resolving all conflicts, stage the resolved files and continue:
  ```bash
  git add -A
  git rebase --continue
  ```
- If a conflict is too ambiguous to resolve automatically, abort the rebase, restore the original state, and tell the user exactly which files need manual resolution:
  ```bash
  git rebase --abort
  ```

### 4. Validate before pushing

Run in sequence — stop and report on any failure:

```bash
make lint
make test
make doc
```

(Skip if already run in step 2 and no rebase changes were introduced.)

### 5. Push

Force-push with lease to update the remote branch safely:

```bash
git push --force-with-lease origin HEAD
```

### 6. Refresh the PR title and body (only if necessary)

Review the current full diff against the base branch:

```bash
git log origin/<base-branch>...HEAD --oneline
git diff origin/<base-branch>...HEAD
```

Draft an updated:
- **Title**: short, imperative sentence summarising the change (≤ 72 chars)
- **Body**: use the template below

Then edit the PR:

```bash
gh pr edit <number> --title "..." --body "$(cat <<'EOF'
## Summary

[1–3 bullet points describing what this PR does and why]

## Changes

[Brief list of the key files / components changed and why]

## Related issues

Closes #<issue-number>   ← remove if no related issue

EOF
)"
```

### 7. Output the PR URL

Run `gh pr view --json url -q .url` and display the URL so the user can open it directly.

## Rules

- Never push if `make lint`, `make test`, `make doc` or `make no-dirty` fail.
- Always use `--force-with-lease` (never bare `--force`) to avoid overwriting concurrent remote changes.
- If the rebase cannot be completed automatically, abort and report — never leave the repo in a conflicted state.
- Preserve the existing PR number; never close and recreate the PR.
