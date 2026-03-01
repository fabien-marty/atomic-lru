# Update an already-opened GitHub Pull Request for the current branch

## Overview

Analyse the current branch state and update the open Pull Request (title + body) using the `gh` CLI.

## Steps

1. **Check for an open PR on the current branch**:
   ```bash
   gh pr view --json number,title,body,url
   ```
   If no PR exists, stop and tell the user to use `/prs/make` instead.

2. **Gather branch context** by running the following in parallel:
   - `git status` — warn the user if there are uncommitted changes
   - `git log main...HEAD --oneline` — list commits on this branch
   - `git diff main...HEAD` — review all changes introduced by this branch
   - `gh issue list --state open` — find related open issues to link

3. **Determine the base branch**: default to `main` unless the branch clearly targets another.

4. **Push any new commits** to the remote:
   ```bash
   git push -u origin HEAD
   ```

5. **Draft the updated PR** based on the full diff and commit history:
   - **Title**: short, imperative sentence summarising the change (≤ 72 chars)
   - **Body**: use the template below

6. **Edit the PR**:
   ```bash
   gh pr edit --title "..." --body "$(cat <<'EOF'
   ## Summary

   [1–3 bullet points describing what this PR does and why]

   ## Changes

   [Brief list of the key files / components changed]

   ## Related issues

   Closes #<issue-number>   ← remove if no related issue

   EOF
   )"
   ```

7. **Output the PR URL** so the user can open it directly.

## Rules

- Never force-push to `main` or `master`.
- DON'T ADD the `AI` label on the PR.
- If there are uncommitted changes, warn the user and stop — do not commit on their behalf.
- If a related GitHub issue is found, link it with `Closes #<number>` in the body.
- Always rewrite both title and body from scratch based on the current diff — do not just patch the existing text.
