# Design

## Technical Approach

Create GitHub Actions workflows in `.github/workflows/`:
- `ci.yml` - runs on every push (lint + test)
- `release.yml` - runs on push to main (lint + test + build + deploy to PyPI)

Use `uv` for fast dependency management and execution.

## Architecture

Components affected:
- `.github/workflows/ci.yml` - continuous integration workflow
- `.github/workflows/release.yml` - release workflow with PyPI deployment
- GitHub Actions secrets (PYPI_TOKEN) needed for deployment

## Constraints

- Requires Python 3.11+ (as per pyproject.toml)
- Uses `hatchling` build backend
- Must use `uv` instead of pip for package management
- PyPI deployment requires repository secret PYPI_TOKEN

## Trade-offs

**Chosen: Separate CI and release workflows**
- Pro: Clear separation of concerns, easier to debug
- Pro: Can run CI on all branches without attempting deployment
- Con: Some duplication between workflows

**Rejected: Single workflow with conditional steps**
- Pro: Less duplication
- Con: More complex logic, harder to read
- Con: Can't easily skip deployment on non-main branches

**Chosen: uv over pip**
- Pro: Faster dependency resolution and installation
- Pro: Better caching
- Pro: Modern tooling as specified in requirements

**Rejected: poetry or pipenv**
- Project uses hatchling, no need for alternative build tool
