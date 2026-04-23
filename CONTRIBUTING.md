# Contributing to SpecInk

Thanks for considering a contribution to SpecInk.

## Philosophy

SpecInk is a tool for spec-driven development. When contributing to SpecInk, **use SpecInk itself** to propose and track your changes. This dogfooding ensures the tool stays practical and catches issues early.

## Getting Started

### 1. Fork and clone

```bash
git clone https://github.com/yourusername/specink.git
cd specink
```

### 2. Install dependencies

SpecInk uses `uv` for dependency management:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install dependencies
uv venv
uv pip install -e ".[dev]"
```

### 3. Run tests

```bash
uv run pytest tests/ -v
```

### 4. Run linters

```bash
uv run ruff check .
uv run ruff format .
uv run mypy specink
```

## Contributing Workflow

### For bug fixes and small changes

1. Create a branch: `git checkout -b fix-something`
2. Make your changes
3. Add tests if applicable
4. Run linters and tests
5. Open a pull request

### For new features or significant changes

Use SpecInk's own workflow:

```bash
# 1. Propose the change
ink propose your-feature-name

# 2. Fill in the proposal and spec
# Edit .specink/changes/your-feature-name/proposal.md
# Edit .specink/changes/your-feature-name/specs/spec.md

# 3. Check for conflicts with other active changes
ink conflicts

# 4. Create a feature branch and implement
git checkout -b your-feature-name
ink apply your-feature-name

# 5. Log key decisions as you work
echo "Reasoning for approach X..." | ink transcript append your-feature-name

# 6. Record architectural decisions
ink decision add your-feature-name

# 7. Verify completion
ink verify your-feature-name

# 8. Archive (optional - maintainer will do this after merge)
ink archive your-feature-name
```

This approach ensures your contribution is well-documented and maintainable.

## Code Standards

### Python version

- **Minimum:** Python 3.11
- **Target:** Python 3.11+

### Code style

- Use `ruff` for linting and formatting (config in `pyproject.toml`)
- Type hints are required (checked with `mypy`)
- Line length: 100 characters
- Follow PEP 8 conventions

### Testing

- Add tests for new features in `tests/`
- Maintain or improve test coverage
- Use `pytest` conventions
- Test files should mirror the structure of `specink/`

### Documentation

- Update README.md for user-facing changes
- Add docstrings for public APIs
- Update CHANGELOG.md under `[Unreleased]`

## Pull Request Process

1. **Branch naming:**
   - Features: `feature/your-feature-name` or `your-feature-name`
   - Fixes: `fix/issue-description`
   - Docs: `docs/what-you-updated`

2. **Commit messages:**
   - Use clear, descriptive messages
   - Start with a verb: "Add", "Fix", "Update", "Remove"
   - Reference issues when applicable: "Fix #123"

3. **PR description:**
   - Explain **why** the change is needed
   - Describe **what** was changed
   - Link to related issues or proposals
   - If you used `ink propose`, reference the change folder

4. **Checklist before submitting:**
   - [ ] Tests pass (`uv run pytest`)
   - [ ] Linters pass (`uv run ruff check .`)
   - [ ] Type checks pass (`uv run mypy specink`)
   - [ ] CHANGELOG.md updated
   - [ ] Documentation updated if needed

## Development Tips

### Running SpecInk locally

After installing with `uv pip install -e ".[dev]"`, the `ink` command will use your local source:

```bash
ink --version  # Uses your local development version
```

### Testing CLI commands

```bash
# Test in a temporary directory
mkdir /tmp/test-specink && cd /tmp/test-specink
ink init
ink propose test-feature
```

### Debugging

Add print statements or use `breakpoint()` in the code, then run:

```bash
uv run pytest tests/test_something.py -v -s
```

## CI/CD

All pull requests run through GitHub Actions:
- Linting with `ruff`
- Type checking with `mypy`
- Tests with `pytest` on Python 3.11 and 3.12

Ensure your changes pass CI before requesting review.

## Questions or Issues?

- **Bug reports:** Open an issue with reproduction steps
- **Feature requests:** Consider running `ink propose <feature-name>` first and sharing the proposal
- **Questions:** Open a discussion or issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
