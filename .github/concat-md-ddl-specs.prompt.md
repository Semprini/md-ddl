You are given a directory named `md-ddl-specification/` containing multiple Markdown specification files.

Use the repo script for one-command generation:

`powershell -ExecutionPolicy Bypass -File .\.github\scripts\concat-md-ddl-specs.ps1`

The above script should create a single output file named `MD-DDL-Complete.md` by concatenating all other specification files in that directory with these rules:

1. Process all `.md` files in deterministic order (alphabetical by filename).
2. For each file:
   - Read all lines.
   - Apart from 1-Foundation.md, remove the first 2 lines.
   - Remove the last 2 lines.
   - Append the remaining lines to `MD-DDL-Complete.md`.
3. Insert exactly one blank line between each file section in the final output.
4. Do not add any extra headers, footers, commentary, or metadata.
5. Preserve original line formatting for all kept lines.

Return only the final combined Markdown content.