# Find issues to fix or improve in the codebase

## Overview

Thoroughly review the entire codebase to identify bugs, improvements, architecture issues, inconsistencies, typos, and any other issues worth fixing. For each finding, create a GitHub issue task with the `Triage` label.

**This command is read-only: DO NOT modify any source file, test, config, or documentation.**

## Labels

Use the following labels depending on the nature of each finding:

- **Bug** — Incorrect behavior, logic errors, unhandled edge cases, race conditions, potential crashes
- **Improvement** — Code quality, performance, readability, missing type hints, better error messages, missing tests, better abstractions
- **Architecture** — Structural issues, coupling, layering violations, import organization, separation of concerns
- **Inconsistency** — Naming inconsistencies, style deviations, API asymmetries, convention violations
- **Typo** — Spelling mistakes, grammar issues in code, comments, docstrings, or documentation
- **Documentation** — Missing, outdated, or misleading documentation, docstrings, or examples

## Steps

1. **Read `AGENTS.md`** to understand the project conventions and constraints.

2. **Search existing github issues** to know what has already been reported. Avoid creating duplicate tasks.

3. **Review the entire codebase systematically.** Read all source files, tests, configuration files, and documentation. 

4. **For each issue found**, create a GitHub issue with:
   - A clear, specific **title**
   - A **description** explaining the issue, where it is (file + approximate location), why it matters, and a suggestion for fixing it
   - **Label**: one of the labels listed above + `AI` + `Triage`
   - **Priority**: `high` for bugs and things that could cause incorrect behavior, `medium` for improvements and architecture issues, `low` for typos and minor inconsistencies

5. **At the end**, display a summary table of all tasks created, grouped by label, showing task ID and title.

## Important rules

- **DO NOT modify any file in the repository.** This command is purely analytical.
- **DO NOT create duplicate tasks.** Always check the existing GitHub issues before creating a new task.
- **Be specific.** Each task should address one concrete, actionable issue — not vague observations.
- **Be honest.** Only report genuine issues, not stylistic nitpicks that conflict with the project's established conventions
- **Group related micro-issues.** If you find multiple typos in the same file or closely related minor issues, group them into a single task rather than creating many tiny tasks.
