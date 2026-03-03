# Implement the next GitHub not-closed issue (with "Planned" label AND without "Human" label)

## Overview

Take the next GitHub not-closed issue (with "Planned" label AND without "Human" label) and implement it.

## Steps

1. Check the next GitHub not-closed issue (with "Planned" label AND without "Human" label). Take high priority issues first.
   - If there is no remaining task OR if labels don't match, STOP at this step with a message "No task found".

2. Display clearly in the output the task you picked (display at least its id and its title).

3. Add the "Status: Implementing" label to the issue and remove the "Status: Planned" label.

4. Execute `git fetch origin main` and then `git rebase origin/main` to update your local branch with the latest changes from the main branch.

5. Execute/implement the task.

6. Open a GitHub pull-request for the task with all your changes.

7. Add the "Status: Implemented" label to the issue but and remove the "Status: Implementing" label.


## Note: 

- NEVER update the body of the issue
