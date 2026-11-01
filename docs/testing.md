# Testing

How the data model was checked before any real record was imported. Two kinds of checks exist: scripted checks on the instance, and manual checks in the forms.

## Scripts

Both files live in `servicenow-scripts/` and are pasted into **System Definition > Scripts - Background** with the application scope selected. They are deliberately not part of the app.

| Script | What it does |
|---|---|
| `gerar_dados_de_teste.js` | Creates invented test data and runs the architecture checks |
| `limpar_dados_de_teste.js` | Removes all test data; has a dry-run switch (`SIMULAR`) |

All the content is invented and every designation starts with `TESTE-`, so cleanup never touches a real record. If test data already exists, run the cleanup script first, because designations are unique and a second run would fail.

**Before committing from Studio:** the scripts make the platform create cross-scope privilege records. Delete them, keeping only `SysUserList` (decision D15).

The seed script has switches at the top (`CONFIG`) to skip any part, for example to build a fully filled record without sections.

## What the checks verify

| Check | Result in the recorded run |
|---|---|
| Default `review_status` is `imported` | Passed |
| Default `text_license` is `cc_by_sa_3_0` | Passed |
| Business Rule sets Needs Review when a record is created with license Other | Passed |
| Business Rule sets Needs Review when the license is changed to Other | Passed |
| A duplicate designation is rejected | Passed |
| Deleting a record deletes its sections | Passed |
| Deleting a record deletes its media | Passed |
| A site with SCPs assigned cannot be deleted (Restrict) | Passed |
| A script can write to the read-only Original Content | Passed |

**9 of 9** passed on the first full run. The duplicate-designation test prints a long database error in the log; that is the expected result of the refusal, not a failure.

## Checked by hand

- A test record showed three sections and two media in the related lists, and the site form listed the record assigned to it.
- Changing a record's license to Other shows the `License Details` field in the form.
- Related lists for SCP Section, SCP Media and Foundation Site were configured and saved into the app (the files appear in the repository).
- Choosing a different license, then back to Other, sends a reviewed record back to Needs Review; editing other fields does not.

## Reference image counts (by hand)

The number of images displayed on each page, counted by looking at the live page. Phase 2 media extraction should reproduce these counts.

| Record | Images on the page |
|---|---|
| SCP-049 | 3 |
| SCP-310 | 3 |
| SCP-359 | 5 |
| SCP-396 | 6 |
| SCP-531 | 4 |
| SCP-736 | 3 |

## Not tested yet

- Whether a script-created record without `title` or `source_url` is rejected (mandatory fields). A ready check can be added to the seed script.
- What a regular user (not an administrator) can see and edit, using *Impersonate User*.
- Writing the largest article (99,688 characters) through the import path, and whether the HTML field sanitises markup on save.
- The import itself: coalesce on the designation, field mapping and choice handling. The first batch of five records is the real test.
