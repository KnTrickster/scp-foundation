# Decisions

Why the project looks the way it does. Each entry gives the context, the decision, what was considered and what follows from it. The evidence behind many of them is in [`discoveries.md`](discoveries.md).

## D1. Validate the data before importing it, and import in small batches

**Context:** The source is a 984-record collection with irregular articles. Importing everything first and cleaning later would hide problems inside the platform.

**Decision:** Understand and check the data with scripts first (titles, gaps, triage, hidden text, media), then import a batch of five records and validate it before widening.

**The five:** SCP-173 (simple, the original test record), SCP-049 (audio and `iframe` modules), SCP-736 (hidden text and a restricted title), SCP-720 (images, audio and video) and SCP-186 (eight images, each with a credit page). They cover the irregular cases without picking the strangest pages.

## D2. Keep the original content apart from the prepared content

**Decision:** `Original Content` holds the page exactly as received. It is read-only in the form; a script can still write to it. `Description` and `Special Containment Procedures` are optional fields filled by extraction.

**Why:** Fields missing from an article, restricted titles and narrative devices must not be corrected or dropped automatically. Keeping the original makes the extraction repeatable and auditable.

**Consequence:** The largest article (SCP-618, 99,688 characters) exceeds the 65,536 shown in the dictionary. A script wrote 100,000 characters successfully; the import path is still to be tested.

## D3. Model the irregular parts as child tables

**Context:** Articles differ a lot: some have many images, some none; some have audio, interviews or extra sections.

**Decision:** `SCP Record` keeps what every article has. `SCP Section` (addenda, interviews, logs) and `SCP Media` hold what varies, one row each, linked by a reference to the record.

**Alternatives considered:**
- *One large field for everything:* simple, but nothing could be queried, related or attributed individually.
- *Many nullable fields on the record:* ugly, and it caps the number of items.

**Consequences:** Irregularity becomes a difference in the number of rows. `SCP Section` separates **Order** (an integer used only for sorting) from **Section Label** (the text the page uses, such as `2.1.3` or `Addendum 1`), so unusual numbering never affects the order. A parent/child hierarchy for sections was left out until the data shows it is needed.

## D4. The designation is the unique key, and the number is a separate field

**Decision:** `SCP Designation` is a mandatory, unique string and the display value. `SCP Number` is an integer, not an auto number: it carries the real number of the SCP.

**Why:** Designations as text sort character by character, so `SCP-1000` would come before `SCP-173`. Series 1 only has three-digit numbers, so this matters from Series 2 on, and for numeric range filters. Unique protects the import from duplicates; it is checked by the database.

## D5. Identity comes from the link, not from the label

**Context:** Three Series 1 entries have labels that differ from their designation (see discoveries, section 2).

**Decision:** The designation is read from the link target. The label is kept as text and is never trusted to identify the article.

**Consequence:** The stored title is the whole label (for example `SCP-173 - ...`). The importer must split off the pure title, and should split at the first ` - ` rather than assume the prefix is `SCP-NNN`.

## D6. Attribution lives on every record

**Decision:** `Author`, `Source URL` and `Text License` are on each record, in their own form tab ("SCP Attribution"). Every media row carries its own author and license.

**Why:** CC BY-SA attribution is per work, not per project, and images often have different terms than the text. A single credits page would not satisfy that. The tab keeps the main form clean without hiding the credit from anyone.

**Consequence:** `Source URL` is mandatory. All 984 records in the inventory have a page URL, so this does not block the import.

## D7. License as a choice with an escape hatch, and a review trigger

**Decision:** `Text License` is a mandatory choice with a default of CC BY-SA 3.0 and one other option, **Other**. Choosing Other shows a `License Details` field (UI Policy *Show license details when Other*). A Business Rule (*Set Review Status when license is Other*) sets `Review Status` to Needs Review when the license changes to Other, using a field action rather than a script.

**Why:** A choice with one option would be a constant. Making exceptions explicit and forcing a review keeps unusual licensing from slipping through.

**Consequences:** The rule fires both when a record is created as Other and when its license is changed to Other, and it does not push a reviewed record back to Needs Review when other fields are edited (tested). The UI Policy runs only in the form, so imports bypass it. The field is labelled for the **text** only; media have their own license field.

## D8. Cascade rules are chosen per relationship

| Reference | Rule | Why |
|---|---|---|
| `SCP Section → SCP Record` | Delete | Sections have no meaning without their record |
| `SCP Media → SCP Record` | Delete | Same |
| `SCP Record → Foundation Site` (`site_location`) | Restrict | A site with SCPs in it must be decommissioned, not deleted |
| `lead_researcher`, `site_director` (users) | Clear | Removing a user must not remove or block SCPs or sites |

All of these were set in the dictionary rather than coded. A deletion Business Rule was considered as a fallback and turned out to be unnecessary. The Delete and Restrict behaviours are covered by tests (see `testing.md`).

## D9. Media are stored as URLs only

**Decision:** `SCP Media` stores the URL, type, caption, author, license and a `Verification Status` (default Pending). No file is downloaded or attached.

**Why:** Licenses for images and audio are individual and sometimes restricted, and some live on third-party sandboxes. Referencing without copying avoids redistributing files whose terms are unverified.

**Consequence.** The API image list undercounts (see discoveries), so media rows in phase 2 are built from the Wikidot source and reconciled with the API list. Records where the two disagree are set to Needs Review and checked by hand against the page.

## D10. Foundation Sites are simplified as basic operational data for the MVP

**Context:** The official SCP Wiki has a complex facility layout (Sites, Areas, Sectors, with multiple specialization prefixes). However, the Series 1 raw text dataset does not provide clean, structured relational data for these, and a textual mention inside an article is not a definitive assignment.

**Decision:** For the first version (MVP) of this application, the `Foundation Site` table is intentionally simplified with basic flat fields (Designation, Type, Status, Region, Director) to serve as operational placeholders. The reference field (`site_location` on the SCP Record) starts empty after an import.

**Why:** A text-mention is not a guarantee of containment. As analyzed in `discoveries.md` (see discoveries, section 7), 68% of the records mention no site at all, and an incident may happen at one site while the object is held at another. Implementing the full wiki facility hierarchy right now would delay the platform's core deployment. Simplifying the fields allows the data model to function immediately, while leaving the architecture open for future refactoring.

**Consequence:** The initial data for Sites will be managed later or even manually. Expanding this table to include the official Wiki prefixes (Areas, Sectors, Armed, Provisional) is documented as technical debt and deferred to the project's Phase 2 Roadmap (still being developed).

## D11. Hidden text is preserved and flagged, never silently removed

**Decision:** Zero-size text is kept in the original content and reported by a script (`texto_oculto.csv`: record, style, size, without the text itself). Any display version is a separate transformation with explicit rules.

**Why:** It is not always junk (discoveries, section 4). One case contains instructions addressed to machine readers, so article text is always handled as data, never as instructions.

## D12. Raw data stays out of the repository

**Decision:** `content_series-1.json` and `index.json` are in `.gitignore` from the first commit. Small derived files (`titulos_serie1.json` and the CSV reports) are committed because they carry designations, titles and counts, not article text.

**Why:** The article text is CC BY-SA content: publishing 984 records means attribution and share-alike for each one, and the files are large. Git history is permanent, so the ignore rule has to exist before the first commit, even in a private repository.

## D13. One private repository, with the app in its own folder

**Decision:** A single repository holds the ServiceNow app, the Python tools, the documentation and the licensing notes. The ServiceNow Studio source-control integration owns one folder (named after the app's sys_id, set by `path=` in `sn_source_control.properties`); everything else lives beside it and is ignored by the integration.

**Rules that make this safe:**
1. Studio commits go to its own branch (`sn_instances/<instance>`) and reach `main` through a pull request merged with a merge commit.
2. The handwritten files (README, scripts, docs) exist only on `main`. `main` is never merged back into the Studio branch, and that branch is never deleted.
3. Nothing inside the app folder is edited by hand.
4. Tags mark safe restore points (`checkpoint-initial-structure`, `checkpoint-structure-complete`).

**Alternative:** Two repositories (one only for the app) remove all risk of the integration touching other files. They stay as the fallback if the single-repository flow causes trouble. The repository stays private until the first records are imported and the licensing notes are settled.

## D14. Naming conventions

ServiceNow artifacts (tables, columns, choice values, rules) use English names. The Python and JavaScript helper scripts use Portuguese identifiers and comments, with an English header or description where a reader would need it. A table in `scp-api-test/README.md` maps each script to a one-line English description.

## D15. Test scripts live outside the app

**Decision:** `servicenow-scripts/` holds a seed script and a cleanup script, pasted into *Scripts - Background* by hand. They are not stored as application files.

**Why:** Running them makes the platform create cross-scope privilege records, which would otherwise be exported with the app. All test data uses a `TESTE-` prefix, so cleanup can never touch real records.

**Routine:** Before every commit from Studio, delete the cross-scope privileges the scripts created, keeping only `SysUserList`.

## D16. A generic default title on sections

`SCP Section.title` has a generic default (`Addendum 1`), chosen on purpose as a base title for sections created by hand. The trade-off is that the field's mandatory flag no longer protects against an empty title, so the importer always sets a real one.

## Open decisions

| # | Question | Notes |
|---|---|---|
| O1 | The 15 index designations with no record: import empty "skeleton" records, or leave them out? | Skeletons would need a title, a URL built from the pattern and Needs Review |
| O2 | Access model | Two roles (`x_1902920_scp_fo_0.admin` and `.user`) and platform-generated ACLs exist; levels by object class and researcher clearance are planned, nothing is verified yet |
| O3 | Importing the largest article | The 99,688-character record is untested through the import path |
| O4 | Mandatory fields during import | Whether a script-created record without `title` or `source_url` is rejected has not been tested |
| O5 | Does Original Content survive on save? | The HTML field may sanitise markup such as `iframe`; compare after importing SCP-049 |
| O6 | Review tasks | Planned: a table extending `Task` and a flow on Review Status = Needs Review |