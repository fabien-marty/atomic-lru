# Plan the next GitHub not-closed issue (with "Status: Validated" label AND without "Human" label)

## Overview

Take the next GitHub not-closed issue (with "Status: Validated" label AND without "Human" label) and analyze it without human intervention (yolo mode).

## Steps

1. Check the next GitHub not-closed issue (with "Status: Validated" label AND without "Human" label). Take high priority issues first.
   - If there is no remaining task OR if labels don't match, STOP at this step with a message "No task found".

2. Display clearly in the output the task you picked (display at least its id and its title).

3. Add the "Status: Planning" label to the issue and remove the "Status: Validated" label.

4. Read the task and plan it. Use any information you find in the task as instructions. Don't ask anything to human (yolo mode) and analyze how you would implement the task.

5. DON'T IMPLEMENT THE TASK! But fill or complete at least the "## Acceptance criteria" and the "## Implementation plan / notes" sections in the GitHub issue.

6. Add the "Status: Planned" label to the task and remove the "Status: Planning" label.
