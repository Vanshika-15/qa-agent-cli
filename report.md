# QA Analysis Report

## Summary
Adds a new `--save` CLI option to the `analyze` command, allowing users to export the generated QA analysis report as a Markdown file.

**Risk Level:** Low

## What to Verify
- Verify that passing a valid file name to `--save` (e.g., `report.md`) correctly writes the Markdown content to disk.
- Verify that running the command without the `--save` option still prints output to the console and does not raise any errors or write files.
- Verify the behavior and error handling when providing a path with a non-existent directory (e.g., `--save non_existent_folder/report.md`).
- Verify permission handling when trying to save to a read-only directory or path without write permissions.
- Verify the formatting of the generated Markdown file, particularly checking how empty lists (like empty `apis_changed`) are rendered using the fallback string.

## APIs / Services Changed
_(none identified)_

## Regression Risk Areas
- Existing CLI execution flow and console output printing (ensuring standard stdout formatting is not disrupted).
- CLI option parsing (verifying there are no conflicts between `--base` and the newly introduced `--save` option).

## Smoke Tests to Run
- Execute `analyze` command with `--save test_smoke.md` and confirm the file is created with expected content.
- Execute `analyze` command without `--save` and confirm the analysis completes successfully with output printed only to the console.
