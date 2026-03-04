# Implement a GitHub issue

## Overview

Take the given GitHub issue and implement it.

## Steps

1. If "$ARGUMENTS" is empty, STOP at this step with a message "No issue provided".

2. Find the given issue: "$ARGUMENTS" in the GitHub issues. Display clearly its id and title.

3. Add the "Status: Implementing" label to the issue and remove any other "Status: *" label.

4. Execute `git fetch origin main` and then `git rebase origin/main` to update your local branch with the latest changes from the main branch.

5. Implement the task following the project conventions in `AGENTS.md`.

6. Don't open a pull-request!

7. Add the "Status: Implemented" label to the issue and remove any other "Status: *" label.


