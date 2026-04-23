# Decisions: Initial Build

## Decision: Use uv instead of pip
**Date**: 2026-04-23
**Status**: Accepted

### What was decided
Use uv as the primary package manager for SpecInk development.

### Rationale
User explicitly requested uv. It's faster than pip and handles virtual environments cleanly with `uv venv` + `uv pip install`.

### Alternatives rejected
- pip - slower, requires manual venv setup

---

## Decision: Extract only confident code identifiers
**Date**: 2026-04-23
**Status**: Accepted

### What was decided
The extract_identifiers() function in spec.py only extracts:
- Backtick-quoted identifiers
- PascalCase with mixed case (e.g., UserAccount)
- snake_case with underscores (e.g., my_function)

### Rationale
Prevents false positives from English words like "called", "set", "THEN". Drift detection needs high-confidence matches only.

### Alternatives rejected
- Extract all lowercase words - too many false positives
- Extract all caps words - matches BDD keywords like GIVEN/WHEN/THEN

---

## Decision: Detect test files by name, not full path
**Date**: 2026-04-23
**Status**: Accepted

### What was decided
The _is_test_file() function checks filename and parent directory name only, not the full path.

### Rationale
Temp test directories contain "test" in their path (e.g., pytest-7/test_check_drift_found0), causing false positives. A file is only a test file if its name or immediate parent contains "test".

### Alternatives rejected
- Check full path for "test" - breaks in test environments
- Only check filename - misses tests/ directory structure

---
