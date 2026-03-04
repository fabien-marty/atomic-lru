# Create a GitHub Pull Request for the current branch

## Overview

Analyze the current branch state, handle uncommitted changes, and create a well-structured GitHub Pull Request using the `gh` CLI.

## Steps

1. **Determine the base branch**: If "$ARGUMENTS" is empty, default to `main`, else use the given base branch: "$ARGUMENTS".

2. **Gather branch context** by running the following in parallel:
   - `git status --short` — detect current branch, untracked/modified files
   - `git branch --show-current` — get the current branch name
   - `gh issue list --state open` — find related open issues to link in the PR

3. **Handle the branch and commits** depending on the current state:

   ### Case A — currently on `main` (or base branch) with uncommitted changes
   - Infer a short, kebab-case branch name from the nature of the changes (e.g. `fix-cache-eviction`, `add-ttl-support`)
   - Create and switch to the new branch:
     ```bash
     git checkout -b <branch-name>
     ```
   - Stage all changes:
     ```bash
     git add -A
     ```
   - Commit with a short imperative message:
     ```bash
     git commit -m "<type>: <short description>"
     ```

   ### Case B — already on a feature branch, with uncommitted changes
   - Stage any new or modified files:
     ```bash
     git add -A
     ```
   - Commit with a short imperative message derived from the diff:
     ```bash
     git commit -m "<type>: <short description>"
     ```

   ### Case C — already on a feature branch, everything committed
   - Nothing to do, proceed to the next step.

4. **Review the full diff** to understand what will go into the PR:
   ```bash
   git log main...HEAD --oneline
   git diff main...HEAD
   ```

5. **Push the branch** to the remote:
   ```bash
   git push -u origin HEAD
   ```

6. **Draft the PR** based on the diff and commit history:
   - **Title**: short, imperative sentence summarising the change (≤ 72 chars)
   - **Body**: use the template below

7. **Create the PR**:
   ```bash
   gh pr create --title "..." --body "$(cat <<'EOF'
   ## Summary

   [1–3 bullet points describing what this PR does and why]

   ## Changes

   [Brief list of the key files / components changed and why]

   ## Related issues

   Closes #<issue-number>   ← remove if no related issue

   EOF
   )"
   ```

8. **Output the PR URL** so the user can open it directly.

## Rules

- If a related GitHub issue is found, link it with `Closes #<number>` in the body.
- Never push a branch if `make lint`, `make test`, `make doc` and `make no-dirty` are not passing
