# AGENTS.md

## Repo Snapshot
- Repository: `jtgsystems/CleanCode`
- Default branch: `master`
- Visibility: `public`
- Summary: Clean code practices - Best practices for writing maintainable code
- Detected stack: Python

## Read First
- `README.md`
- `CLAUDE.md`
- `setup.py`
- `.github/workflows/`

## Key Paths
- `logs/`

## Working Rules
- Keep changes focused on the task and match the existing file layout and naming patterns.
- Update tests and docs when behavior changes or public interfaces move.
- Do not commit secrets, credentials, ad-hoc exports, or large generated artifacts unless the repository already tracks them intentionally.
- Prefer the existing automation and CI workflow over one-off commands when both paths exist.
- Legacy agent guidance exists in `CLAUDE.md`; keep it aligned with `AGENTS.md` if those files remain in use.

## Verified Commands
- Install: `python -m pip install -e .`
- Build: `python -m build`

## Change Checklist
- Run the relevant tests or static checks for the files you changed before finishing.
- Keep human-facing docs aligned with behavior changes.
- If the repo has specialized areas later, add nested `AGENTS.md` files close to that code instead of overloading the root file.

## Notes
- CI source of truth lives in `.github/workflows/`.

This file should stay short, specific, and current. Update it whenever the repo's real setup or verification steps change.
