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
