# Plan the next GitHub not-closed issue (with "Status: Validated" label AND without "Human" label)

## Overview

Take the next GitHub not-closed issue (with "Status: Validated" label AND without "Human" label) and plan it (in plan mode).

## Steps

1. Check the next GitHub not-closed issue (with "Status: Validated" label AND without "Human" label). Take high priority issues first.
   - If there is no remaining task OR if labels don't match, STOP at this step with a message "No task found".

2. Display clearly in the output the task you picked (display at least its id and its title).

3. Add the "Status: Planning" label to the issue and remove the "Status: Validated" label.

4. Switch to plan mode.

5. Read the task and plan it. Use any information you find in the task as instructions. You can ask the human questions if anything is not clear enough. Present your plan to the human and wait for an explicit validation before continuing.

6. DON'T IMPLEMENT THE TASK! After the human validation, use the validated plan to fill or complete at least the "## Acceptance criteria" and the "## Implementation plan / notes" sections in the GitHub issue.

7. Add the "Planned" label to the task but don't remove the "In Progress" label.
   - If the human rejects the plan and no path forward is agreed, remove the "In Progress" label instead.
