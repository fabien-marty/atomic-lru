# Create a GitHub Pull Request for the current branch

## Overview

Analyze the current branch state and create a well-structured GitHub Pull Request using the `gh` CLI.

## Steps

1. **Gather branch context** by running the following in parallel:
   - `git status` — check for uncommitted changes (warn the user if any)
   - `git log main...HEAD --oneline` — list commits on this branch
   - `git diff main...HEAD` — review all changes introduced by this branch
   - `gh issue list --state open` — find related open issues to link in the PR

2. **Determine the base branch**: default to `main` unless the branch clearly targets another.

3. **Push the branch** to the remote if not already pushed:
   ```bash
   git push -f -u origin HEAD
   ```

4. **Draft the PR** based on the diff and commit history:
   - **Title**: short, imperative sentence summarising the change (≤ 72 chars)
   - **Body**: use the template below

5. **Create the PR**:
   ```bash
   gh pr create --title "..." --body "$(cat <<'EOF'
   ## Summary

   [1–3 bullet points describing what this PR does and why]

   ## Changes

   [Brief list of the key files / components changed]

   ## Related issues

   Closes #<issue-number>   ← remove if no related issue

   EOF
   )"
   ```

6. **Output the PR URL** so the user can open it directly.

## Rules

- Never force-push to `main` or `master`.
- DON'T ADD the `AI` label on the PR.
- If there are uncommitted changes, warn the user and stop — do not commit on their behalf.
- If a related GitHub issue is found, link it with `Closes #<number>` in the body.
