# Plan the next GitHub not-closed issue (without "Human" label AND without "Triage" label AND without "In Progress" label)

## Overview

Take the next GitHub not-closed issue (without "Human" label AND without "Triage" label AND without "In Progress" label) and plan it (in plan mode).

## Steps

1. Check the next GitHub not-closed issue (without "Human" label AND without "Triage" label AND without "In Progress" label). Take high priority issues first.
   - If there is no remaining task OR if remaining tasks have the "Human" or "Triage" or "In Progress" label, STOP at this step with a message "No task found".

2. Display clearly in the output the task you picked (display at least its id and its title).

3. Add the "In Progress" label to the issue.

4. Switch to plan mode.

5. Read the task and plan it (in plan mode). Use any information you find in the task as instructions. You can ask the human questions if anything is not clear enough. Present your plan to the human and wait for an explicit validation before continuing.

6. DON'T IMPLEMENT THE TASK! After the human validation, use the validated plan to fill or complete at least the "## Acceptance criteria" and the "## Implementation plan / notes" sections in the GitHub issue.

7. Add the "Planned" label to the task but don't remove the "In Progress" label.
   - If the human rejects the plan and no path forward is agreed, remove the "In Progress" label instead.
