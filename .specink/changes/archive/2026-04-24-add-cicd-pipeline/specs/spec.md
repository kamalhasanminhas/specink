# Specification

## Requirements
  - Automated linting (ruff), type checking (mypy), tests (pytest) on every push
  - Support python 3.11 and 3.12
  - PyPI publishing on push to main
  - Secure token-based authentication for PyPI

## Scenarios

**GIVEN** a PR is opened with code changes
**WHEN** CI workflow runs
**THEN** ruff linting passes
**AND** mypy type checking passes
**AND** pytest runs successfully on Python 3.11 and 3.12

**GIVEN** changes are merged to main branch
**WHEN** release workflow triggers
**THEN** package is build with uv build
**AND** package is published to PyPI with uv publish
**AND** PYPI_TOKEN secret is used for authentication