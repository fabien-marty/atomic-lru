# AGENTS.md - AI Agent Guide for atomic-lru

This document provides essential context and guidelines for AI agents working on the `atomic-lru` codebase.

## Execute linting (style, type checking, import checking...) including some automatic fixes

Execute `make lint` to execute all these linting/fixing tools. Don't propose any changes if the linting fails (exit code different from 0).

## Execute tests

Execute `make test` to execute the tests. Don't propose any changes if the tests fail (exit code different from 0).

Notes:

- we use `pytest` for testing
- we don't want use mocks for testing (unless it's really necessary)
- we prefer function-based tests over class-based tests

## Execute documentation generation

Execute `make doc` to generate the documentation. Don't propose any changes if the documentation generation fails (exit code different from 0).

Don't modify `README.md` file directly as it is generated from the `README.md.template` file (and other files).

## Issues management

We use GitHub Issues to manage the issues. To list, edit, create issues, use the `gh` command line tool. When creating an issue, add the `Reporter: AI` label to it.

## Standardized labels

We use the following standardized labels.

### For issues only

- `Reporter: AI` - Issues created by AI agents

- `Status: Validated` - Issues that have been validated and that are ready to be planned/implemented
- `Status: Planning` - Issues that are being worked on in planning mode
- `Status: Planned` - Issues with a validated plan
- `Status: Implementing` - Issues that are being implemented
- `Status: Implemented` - Issues that have been implemented (in a pull-request or in a local branch)

### For issues AND pull-requests

- `Type: Added` - Issues that are new features 
- `Type: Changed` - Issues that are changes to existing features
- `Type: Removed` - Issues that are removals of existing features
- `Type: Fixed` - Issues that are bug fixes
- `Type: Security` - Issues that are security issues
- `Type: Dependencies` - Issues that are dependencies changes
- `Type: Documentation` - Issues that are documentation changes
- `Priority: Critical`
- `Priority: High`
- `Priority: Medium`
- `Priority: Low`

Issues MUSTN'T have multiple `Status: *` or `Priority: *` or `Type: *` labels at the same time.

## Coding Conventions

### Type Hints
- **Always** use type hints (Python 3.10+ features)
- Use `|` for union types (e.g., `int | None`, not `Optional[int]`)
- Use `Protocol` for structural subtyping (e.g., `Serializer`, `Deserializer`)

### Comments

- **Always** Python style comments when adding doctrings
- When adding examples in docstrings, use this format:

Example:
    ```python
    import os
    print(os.getcwd())
    ```

- Don't use `>>>` in docstrings
