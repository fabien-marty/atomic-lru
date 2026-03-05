# Find issues to fix or improve in the codebase

## Overview

Thoroughly review the ENTIRE codebase to identify bugs, improvements, architecture issues, inconsistencies, typos, and any other issues worth fixing. For each finding, create a GitHub issue with the `Reporter: AI` label.

**This command is read-only: DO NOT modify any source file, test, config, or documentation.**

## Steps

1. **Read `AGENTS.md`** to understand the project conventions and constraints.

2. **Search existing github issues** to know what has already been reported. Avoid creating duplicate tasks.

3. **Review the entire codebase systematically.** Read all source files, tests, configuration files, and documentation.

4. **For each issue found**, create a GitHub issue with:
   - A clear, specific **title**
   - A **description** explaining the issue, where it is (file + approximate location), why it matters, and a suggestion for fixing it
   - **Label**: `Reporter: AI` + `Type: ...` + `Priority: ...` (never add a `Status: ...` label when creating an issue)

5. **At the end**, display a summary table of all tasks created, grouped by label, showing task ID and title.

## Important rules

- **DO NOT modify any file in the repository.** This command is purely analytical.
- **DO NOT create duplicate tasks.** Always check the existing GitHub issues before creating a new task.
- **Be specific.** Each task should address one concrete, actionable issue — not vague observations.
- **Be honest.** Only report genuine issues, not stylistic nitpicks that conflict with the project's established conventions
- **Group related micro-issues.** If you find multiple typos in the same file or closely related minor issues, group them into a single task rather than creating many tiny tasks.
- **It's OK if you don't find any issue!** In that case, just display a message "No issue found".
