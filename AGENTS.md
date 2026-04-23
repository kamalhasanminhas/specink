# SpecInk — AI assistant instructions

This project uses SpecInk for Spec-Driven Development.
All changes follow the workflow: propose → apply → verify → archive.

## Active changes
Run `ink list` to see all active changes and their current state.

## Starting a new feature
1. Run `ink propose <name>` to create the change folder
2. Review and edit `.specink/changes/<name>/proposal.md`
3. Fill in `.specink/changes/<name>/specs/spec.md` with BDD scenarios
4. Fill in `.specink/changes/<name>/design.md` with technical approach
5. Break work into tasks in `.specink/changes/<name>/tasks.md`

## Logging your session
Append key decisions and reasoning to the transcript:
`ink transcript append <name> --speaker assistant`

## Recording design decisions
When you choose one approach over alternatives, record it:
`ink decision add <name>`

## Finishing a change
Run `ink verify <name>` to confirm all tasks are complete.
Run `ink archive <name>` to merge specs into `.specink/specs/` and archive.

## Checking for drift
Run `ink drift` to check if archived specs match the current codebase.
