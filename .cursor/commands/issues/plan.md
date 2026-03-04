# Plan a GitHub issue

## Overview

Take the given GitHub issue and plan it (in plan mode).

## Steps

1. If "$ARGUMENTS" is empty, STOP at this step with a message "No issue provided".

2. Find the given issue: "$ARGUMENTS" in the GitHub issues. Display clearly its id and title.

3. Add the "Status: Planning" label to the issue and remove any other "Status: *" label.

4. Switch to plan mode.

5. Read the task and plan it. Use any information you find in the task as instructions. You can ask the human questions if anything is not clear enough. Present your plan to the human and wait for an explicit validation before continuing.

6. DON'T IMPLEMENT THE TASK! After the human validation, use the validated plan to fill or complete at least the "## Acceptance criteria" and the "## Implementation plan / notes" sections in the GitHub issue.

7. Add the "Status: Planned" label to the issue and remove any other "Status: *" label.
   - If the human rejects the plan and no path forward is agreed, remove the "Status: Planning" label and restore the previous "Status: *" label instead.
