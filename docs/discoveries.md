# Discoveries

What the data and the platform taught us while preparing the SCP Foundation app. Most of these findings changed a decision; those links are noted in [`decisions.md`](decisions.md).

## 1. Where the data comes from

The article data comes from the [scp-data](https://github.com/scp-data) project, which publishes a dataset of SCP articles and metadata built by crawling the wiki (`scp-api` is the dataset, `scp_crawler` is the crawler). Two files are used:

| File | What it is |
|---|---|
| `content_series-1.json` | One record per Series 1 article |
| `index.json` | The wiki's hub pages as HTML; only the `scp-series` hub is used |

Neither file is committed to this repository (decision D12). `scp-api-test/data/README.md` explains how to obtain them.

- **Snapshot date:** 22 Oct 2026
- **Dataset terms:** The automation tools and crawling scripts provided by the `scp-data` organization operate under the MIT License. However, their dataset documentation explicitly clarifies that they do not claim ownership over the scraped data; all extracted article text and wiki content remain strictly subject to the original Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) license, as recorded in [`LICENSES.md`](../licenses/LICENSES.md).

Each record carries identification fields (`scp`, `scp_number`, `title`, `link`, `url`), the article as HTML (`raw_content`), the Wikidot source (`raw_source`), and metadata (`images`, `history`, `references`, `tags`, `hubs`).

The `images` list is **not** a complete media inventory. Audio, video and embedded modules show up only in the HTML or in the source.

## 2. Counting Series 1: the three missing titles

The first title extractor read the designation from the visible text of each hub entry (`SCP-173 - ...`). It found **996** titles, but Series 1 has 999 designations, so three were missing. All three had something unusual:

| Designation | Why it was skipped |
|---|---|
| SCP-213 | The hub label reads `PDG-213`, even though the link points to `/scp-213` |
| SCP-356 | The hub label reads `SCP-USA64-356`, with the same `/scp-356` link |
| SCP-902 | The link points to `/902-warning` instead of `/scp-902` |

The extractor had silently discarded them: the label did not match, so the entry was dropped without a message. The fix was to **take identity from the link target and treat the label only as text**. The result is **999** titles, and the validator reports no missing numbers between 1 and 999. Five hub links that are not articles are ignored on purpose (`/universe-hub`, `/scp-hub`, `/audio-adaptations`, `/scp-series-tales-edition`, `/scp-series-1-tales-edition`).

The extractor now prints what it ignores, and that report is what made the second diagnosis possible. The lesson is simple: a `continue` that drops data without saying so is a bug waiting to happen.

### Reconciling the numbers

| What | Count |
|---|---|
| Designations in the index (SCP-001 to SCP-999) | 999 |
| Records in the collection | 984 |
| Index designations with no record in the collection | 15 |
| Records with no index title | 0 |
| Collection keys that are not `SCP-*` | 0 |

999 − 15 = 984.

The 15 designations present in the index but not in the collection: SCP-001, 029, 050, 161, 179, 206, 321, 528, 573, 590, 693, 721, 834, 894 and 963.

- **SCP-001** is a special case: on the wiki it is a set of independent proposals rather than a single article. Its index label also carries a "blocked" marker.
- For the other 14 the reason is unknown. They were searched for in every identification field of the collection (key, `scp`, `scp_number`, `link`, `url`) and not found.
- Absence from this collection does not mean absence from the wiki. It only means the page is not in the file that was analysed.

## 3. Titles that need a human

The triage flagged **13** of 999 titles for manual review: 12 labels ending in `N/A`, and SCP-736, whose index title reads `[ACCESS DENIED]`.

SCP-736's content is long (about 51,700 characters) despite the restricted title, so a restricted title is not an empty article. These are signals for review, never reasons for automatic exclusion.

Known gap: the triage indicator list does not include the `[Blocked]` marker seen on SCP-001.

## 4. Hidden text

A scan for inline styles with a zero font size found **32 elements in five records**:

| Record | What the hidden content looks like |
|---|---|
| SCP-231 | The bulk of the findings: many short verse-like passages and scripture references, plus a message addressed to the reader |
| SCP-696 | One short passage |
| SCP-736 | A note addressed to automated readers, telling them how to interpret the page |
| SCP-947 | Navigation links to other hubs and pages |
| SCP-948 | Two elements: a leftover test note from the page’s author, and a hidden backlinks module (navigation) |

What this taught us:

- Hidden does not mean junk. Some of it is narrative, some is page structure, and one case is an instruction aimed at machine readers.
- The original HTML has to be preserved. Any display version is a separate, rule-based transformation with manual review.
- **Page content is data, never instructions.** SCP-736 shows why this matters for any later automation that hands article text to a language model.
- The scan only sees inline `font-size: 0` styles. Text hidden through CSS classes, `display: none` or matching colours would not be found.

## 5. Media

The media inventory (no files were downloaded) analysed **984** records:

| Finding | Records |
|---|---|
| With images in the API `images` field | 374 |
| With audio URLs | 6 |
| With video URLs | 1 |
| Flagged for manual review | 29 |

Audio appears in SCP-049 (4 files), SCP-216 (1), SCP-474 (6), SCP-682 (1), SCP-720 (1) and SCP-884 (1). The only video is in SCP-720. SCP-474 lists tracks 1A to 5A and 7A, with no 6A.

Observations that shaped the model:

- **Wikimedia Commons links are credit pages, not files.** SCP-186 has eight images and one credit page for each, which is the data needed to fill author and license per image.
- **Some images live on third-party sandbox sites** (SCP-255, SCP-359). Their licenses need individual verification.
- **Pages reference files from other places.** SCP-720's list includes a file from another article's folder, and SCP-102's includes a theme logo. The `images` field is cleaner than the URLs scraped from the HTML.
- **Four pages have `iframe` modules but no recognised media:** SCP-245, 506, 819 and 924. They need manual review.
- **Images the API does not list.** The API `images` field undercounts, and so does the URL inventory. On six pages counted by hand, the API listed 2 of 3 images (SCP-049), 1 of 3 (SCP-310), 4 of 5 (SCP-359), 2 of 6 (SCP-396), 1 of 4 (SCP-531) and 2 of 3 (SCP-736). Many images are declared in the Wikidot source only by file name (for example `|url=049_2_ntsc.png`) instead of a full URL. Reading the images declared in the source matched the displayed count on five of the six pages and was one too many on SCP-396 (7 declared, 6 displayed). Across the collection, the source declares images that neither the API nor the URL inventory sees in 11 of 984 records (18 files), including SCP-049 and SCP-736 from the first import batch. The 12 files in the five hand-checked records were all images displayed on the page. The URL inventory also miscounts in both directions (7 against 3 for SCP-736, 2 against 4 for SCP-531), because it picks up credit pages and files from other articles while missing images declared by name. Counts were taken on the live pages, which may differ from the snapshot. Media extraction in phase 2 therefore reads the Wikidot source, keeps file names exactly as written, and sends records where the sources disagree to review.

A regex mistake taught a useful lesson. A tweak that also matched protocol-relative URLs (`//host/path`) caught Wikidot's italics markup (`//text//`) as if it were URLs, and the standard URL parser then crashed on one of them. The tweak was reverted, and the extension is now read with plain string handling instead of a full URL parser.

## 6. How big are the articles?

Largest `raw_content` values:

| Record | Characters |
|---|---|
| SCP-618 | 99,688 |
| SCP-900 | 58,592 |
| SCP-643 | 56,876 |
| SCP-736 | 51,685 |
| SCP-821 | 50,588 |
| SCP-186 | 48,749 |
| SCP-255 | 38,412 |
| SCP-228 | 37,898 |
| SCP-342 | 37,776 |
| SCP-039 | 37,073 |

Only SCP-618 is above the 65,536 characters shown in the field's dictionary entry. A background script wrote 100,000 characters into Original Content and read the same 100,000 back, so the stated limit was not enforced on that path. Whether the import path behaves the same is still untested, and so is whether the HTML field sanitises markup such as `iframe` on save.

## 7. Where do the articles say they are?

The lists of facilities are loose in the text. **316 of 984 records** mention some `Site-N`:

| Site | Records |
|---|---|
| Site-19 | 88 |
| Site-17 | 33 |
| Site-23 | 13 |
| Site-77 | 12 |
| Site-66 | 11 |
| Site-76 | 8 |
| Site-73 | 6 |
| Site-11, Site-15, Site-16 | 5 each |

668 records (68%) mention no site at all, and a mention is not the same as an assignment: an incident may happen at one site while the object is held at another. This is why site allocation is manual (decision D10).

## 8. Platform findings (ServiceNow, Zurich)

- **Reference cascade rule** lives in the *Advanced view* of the dictionary entry, not in the default view. The rule offers None, Delete, Clear and Restrict among its options.
- **Unique** is enforced by the database. The duplicate designation test produced a database error and the insert was refused.
- **Restrict** produces a readable message naming the record that blocks the deletion.
- **Read-only** on a field blocks edits in the form but not writes by a script.
- **Scripts run in Scripts - Background create cross-scope privilege records** on their own. They are application files, so they end up in the next export unless deleted first.
- **Linking an app to source control** warns that completed update sets and customer update records are deleted. The default branch is named after the instance (`sn_instances/<instance>`). The app is exported to a folder named after its sys_id, and `sn_source_control.properties` records the path to that folder.
- **The platform's own README** inside the app folder warns about changes made outside the instance (the folder carries a checksum). The practical rule is never to edit that folder by hand (decision D13).
- **Related lists** in forms are saved as application files (`sys_ui_related_*`), so they travel with the app.
- **Commit dialog:** the option "Include changes not tracked via the Customer Update table" exists because some changes do not create tracked records; it is ticked for full snapshots.