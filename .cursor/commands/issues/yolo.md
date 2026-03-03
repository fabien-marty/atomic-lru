# Implement the given GitHub issue

## Overview

Take the given GitHub issue and implement it.

## Steps

1. If "$ARGUMENTS" is empty, STOP at this step with a message "No issue provided".

2. Execute `test -f .git && echo "WORKTREE"`. If the command does not output "WORKTREE", STOP at this step with a message "Launch this command in a git worktree".

3. Find the given issue: "$ARGUMENTS" in the GitHub issues. Display clearly its id and title.

4. If the label is "Status: Planning", "Status: Planned", or "Status: Implementing", jump directly to step 9. Else, continue to step 5.

5. Add the "Status: Planning" label to the issue and remove any other "Status: *" label.

6. Read the task and plan it. Use any information you find in the task as instructions. Don't ask anything to human (yolo mode) and analyze how you would implement the task.

7. DON'T IMPLEMENT THE TASK FOR THE MOMENT! But fill or complete at least the "## Acceptance criteria" and the "## Implementation plan / notes" sections in the GitHub issue.

8. Add the "Status: Planned" label to the task and remove any other "Status: *" label.

9. Add the "Status: Implementing" label to the issue and remove any other "Status: *" label.

10. Execute `git fetch origin main` and then `git rebase origin/main` to update your local branch with the latest changes from the main branch.

11. Implement the task following the project conventions in `AGENTS.md`.

12. Open a GitHub pull-request for the task with all your changes.

13. Add the "Status: Implemented" label to the issue and remove any other "Status: *" label.
