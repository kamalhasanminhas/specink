# Tasks

## Implementation Checklist

- [x] Create `.github/workflows` directory
- [x] Create `ci.yml` workflow (lint + test on every push)
- [x] Create `release.yml` workflow (lint + test + build + deploy on main)
- [ ] Test CI workflow triggers correctly
- [x] Document PYPI_TOKEN secret requirement

## Verification

- [ ] CI workflow runs on push to any branch
- [ ] CI workflow runs lint (ruff) successfully
- [ ] CI workflow runs tests (pytest) successfully
- [ ] CI workflow runs type checking (mypy) successfully
- [ ] Release workflow only runs on push to main
- [ ] Build step produces valid wheel and sdist
- [ ] Deployment step configuration is correct (pending PYPI_TOKEN)
