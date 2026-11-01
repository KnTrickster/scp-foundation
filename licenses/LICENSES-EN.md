# Licensing and attribution

This project is an application built on the ServiceNow platform, inspired by the SCP Foundation universe. It is an independent learning and portfolio project (see section 7).

## 1. SCP Wiki content

The SCP universe is written and maintained by a community of authors. Wiki content is licensed under [Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/), under the conditions the wiki describes.

- **Source:** [SCP Foundation Wiki](https://scp-wiki.wikidot.com/)
- **Licensing guide:** [Licensing Guide](https://scp-wiki.wikidot.com/licensing-guide)
- **License:** [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

Attribution for individual articles, authors and assets is recorded in the sections below. **This repository contains no article text.** The raw data files are excluded on purpose (see [`docs/decisions.md`](../docs/decisions.md), decision D12).

## 2. Where the data was obtained

Article data was obtained from the [scp-data](https://github.com/scp-data) project, a dataset built by crawling the wiki. The dataset's documentation states that it is not affiliated with the SCP Wiki or its administrators and that all wiki content in it is subject to the wiki's license. The terms of the wiki therefore apply to the data.

See [`scp-api-test/data/README.md`](../scp-api-test/data/README.md) for how to obtain the files and which snapshot was used.

## 3. Derived data files in this repository

| Files | What they contain |
|---|---|
| `scp-api-test/data/titulos_serie1.json` | SCP designations and the title labels of the wiki's Series 1 index |
| `scp-api-test/reports/*.csv` | Designations, title labels, media and page URLs, image file names, counts and flags |

None of them contains article text. These files are shared under CC BY-SA 3.0, with attribution to the SCP Wiki and to the scp-data project.

## 4. Visual assets

Each external asset is documented individually.

| Asset | File | Author | Source | License | Modifications |
|---|---|---|---|---|---|
| SCP Foundation logo | `system-images/logos/SCP_Foundation_(emblem).svg` | far2 / Aelanna | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SCP_Foundation_(emblem).svg) | CC BY-SA 3.0 | None |
| SCP-173 redesign | `system-images/scp-records/scp-173_grimbuscula.png` | [@Grimbuscula](https://x.com/Grimbuscula) | [SCP-173 redesign gallery](https://scp-wiki.wikidot.com/scp-173-redesign-collab-hub-subpage-4) | CC BY-SA 3.0 | None |

Assets whose author or license has not been confirmed are not included in the repository.

**Screenshots.** Images in `system-images/system-screenshots/` show the ServiceNow application and may include wiki text or images. Each one is credited in its caption.

## 5. Works used

One entry per article used.

| Title | Author | Original URL | License | Use | Modifications |
|---|---|---|---|---|---|
| SCP-173 | Moto42 | https://scp-wiki.wikidot.com/scp-173 | CC BY-SA 3.0 | Reproduction in a private ServiceNow instance, for study. Not part of this repository | None |

When article text is imported, each record carries its own `Author`, `Source URL` and `Text License` fields (see [`docs/decisions.md`](../docs/decisions.md), decision D6).

## 6. Code and original contributions

The code, the technical structure and the documentation written for this project are identified separately from third-party material and from content derived from the SCP universe.

They are licensed under the [MIT License](../LICENSE). The MIT License does **not** cover wiki content, the derived data files in section 3 or the third-party assets in section 4, which keep the licenses stated above.

<!-- After contacting the wiki's Licensing Team, add the date and any guidance received here. -->

## 7. Independence

This is an independent project, built for learning and as a portfolio piece. It is not an official SCP Foundation Wiki product and does not imply approval or sponsorship by its authors or contributors. ServiceNow is a trademark of ServiceNow, Inc.; this project is not affiliated with or endorsed by it.

---

*This document is updated as new sources, assets and contributions are added.*