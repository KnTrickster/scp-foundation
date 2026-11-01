# SCP Foundation — Secure, Contain, Protect

A ServiceNow application that turns the SCP Foundation universe into a fictional operations system: anomalous objects, their sections and media, and the facilities that hold them, with review workflows built on top.

**Platform:** ServiceNow (Personal Developer Instance, Zurich) · **Scope:** `x_1902920_scp_fo_0` · **Status:** in development

> An independent learning and portfolio project. It is not an official SCP Foundation Wiki product and has no affiliation with the wiki, its authors or its staff. ServiceNow is a trademark of ServiceNow, Inc. See [`licenses/LICENSES.md`](licenses/LICENSES.md).

## Why this project exists

I wanted to learn ServiceNow by building something real rather than following exercises. The SCP universe is a good fit: it is structured enough to model (records, classes, facilities, procedures), irregular enough to be a genuine data problem, and it is a community project with clear licensing rules that I had to respect.

It started as a table and one test record. It became a lesson in data modelling, in checking data before trusting it, and in treating licensing as part of the design. Those lessons are written down in [`docs/discoveries.md`](docs/discoveries.md) and [`docs/decisions.md`](docs/decisions.md).

## Where it stands

**Built and tested**

- A scoped application with four related tables (below), with forms, lists, list views (Operations and Curation) and related lists
- A UI Policy that shows a license-details field when the license is *Other*, and a Business Rule that sets the review status to *Needs Review* when the license changes to *Other*
- Cascade rules chosen per relationship (Delete, Restrict, Clear)
- Version control through the Studio source-control integration with GitHub
- A seed and a cleanup script in JavaScript: 9 of 9 architecture checks passed ([`docs/testing.md`](docs/testing.md))
- Python tools that validated the Series 1 data (999 designations, 984 records) before any import ([`scp-api-test/`](scp-api-test/))

**Not yet**

- Importing real records (the first batch is the next step)
- Custom roles and ACLs (the platform generated a basic set)
- Review tasks, incidents, dashboards and a user-facing portal page
- Refactor the Foundation Site table into a multi-tier hierarchy (separating Sites from Areas and adding specialized prefixes) to fully align with the official Secure Facilities Locations wiki lore.
## The data model

| Table | What it holds | Notable fields |
|---|---|---|
| **SCP Record** | One row per SCP | Designation (unique), number, title, object class, containment procedures, description, original content (read-only), author, source URL, text license, review status, lead researcher, site location |
| **SCP Section** | The irregular parts of an article: addenda, interviews, logs | Record (cascade delete), type, order, label, title, content |
| **SCP Media** | Images, audio and video, stored as URLs only | Record (cascade delete), type, caption, author, license, verification status |
| **Foundation Site** | Facilities | Designation (unique), type, status, region, director |

Relationships: one record has many sections and many media; one site holds many records (a site with records cannot be deleted).

The reasoning behind each choice is in [`docs/decisions.md`](docs/decisions.md).

*Screenshot of the SCP Record form: coming after the first import.*

<!-- ![SCP Record form](system-images/system-screenshots/scp-record-form.png) -->


*Screenshot of the Lists and Related Lists: coming after the first import.*
<!-- ![SCP Lists and Related Lists](system-images/system-screenshots/lists-and-related-lists.png) -->


## Repository layout

```text
.
├── 02777a4897c057109663b73de053afa2/   ServiceNow app files, managed by Studio (do not edit by hand)
├── docs/                               discoveries, decisions and testing notes
├── licenses/                           licensing and attribution
├── scp-api-test/                       Python data-preparation tools
├── servicenow-scripts/                 JavaScript test scripts, run by hand in Scripts - Background
├── system-images/                      logo and record images, each credited in LICENSES.md, screenshots will be added as the project advances
├── sn_source_control.properties        written by ServiceNow; points to the app folder
└── README.md
```

The folder with the long hexadecimal name is the application itself, named after its internal id and exported by the Studio source-control integration. The rest of the repository sits beside it and is ignored by that integration. The branch workflow that keeps the two apart is described in decision D13.

## About the data

The article data comes from the [scp-data](https://github.com/scp-data) dataset. **No article text is committed here.** The raw files stay out of the repository, and [`scp-api-test/data/README.md`](scp-api-test/data/README.md) explains how to obtain them and which snapshot was used.

## Roadmap

1. **Import the first batch of five records** (SCP-173, 049, 736, 720 and 186, chosen to cover the irregular cases) with an Import Set and a Transform Map, and validate them against the wiki
2. Extract sections and media for those records
3. A review flow: a task table extending `Task`, driven by *Review Status = Needs Review*
4. Roles and ACLs by object class, with a clearance level for researchers
5. Incidents, dashboards and a user-facing page

## How this was built

I'm Systems Analysis and Development student, and this is my first larger ServiceNow project. I used AI assistants (Claude and ChatGPT) throughout as mentors and pair-programmers: to explain concepts, review my scripts and suggest improvements. The aim was to learn faster and catch mistakes earlier while I build experience and . I compared every script's output with the live wiki, and built and tested the application in the instance myself. The reasoning behind each design choice is in [`docs/decisions.md`](docs/decisions.md).

## Licensing

- Wiki Content: CC BY-SA 3.0, attributed in [`licenses/LICENSES.md`](licenses/LICENSES.md)
- Code and Documentation: [MIT License](LICENSE).

## Author

Kevin Torquato · [GitHub](https://github.com/KnTrickster) · [LinkedIn](https://www.linkedin.com/in/kt-1830a52b7)

<sub>If you find an error, information that needs updating, or have any suggestions, please feel free to reach out. I'm all ears and always looking for real improvement! ;)</sub>