You are given a directory named `md-ddl-specification/` containing MD-DDL section files.

Use the repo script for one-command generation:

`powershell -ExecutionPolicy Bypass -File .\.github\scripts\concat-md-ddl-specs.ps1`

The script must generate `md-ddl-specification/MD-DDL-Complete.md` using these exact rules:

1. Input files:
   - Include only section files `1-Foundation.md` through `10-Adoption.md`.
   - Exclude `MD-DDL-Complete.md` from inputs.
2. Order:
   - Concatenate in deterministic section order: `1` to `10`.
3. Heading handling:
   - Preserve one top-level H1 from `1-Foundation.md`.
   - For each section body, remove the first 2 lines (repeated section heading + subtitle line).
4. Trailing navigation handling:
   - Remove the trailing nav block only when present, by pattern (not fixed line count):
     - optional blank lines
     - `---`
     - optional blank lines
     - `...next: Section -> next-file-name.md`
   - Do not assume every section has this block; `10-Adoption.md` may not.
5. Output formatting:
   - Insert exactly one blank line between concatenated section bodies.
   - Do not add any extra headers, footers, commentary, or metadata.
   - Preserve original line formatting for kept lines.
   - Write UTF-8 so Unicode punctuation remains valid.

Post-generation verification checklist:

1. `MD-DDL-Complete.md` begins with `# MD‑DDL Specification (Draft X.Y.Z)` from `1-Foundation.md`.
2. No `...next:` navigation lines remain in the output.
3. Section headings `## **Domains**` through `## **Adoption**` are present.
4. Exactly one blank line separates concatenated section bodies.
5. File is valid UTF-8 and preserves Unicode punctuation used by the source files.

Return only the final combined Markdown content when asked to output content directly.
