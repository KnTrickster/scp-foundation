# Data-preparation tools

Python scripts used to understand and check the SCP data **before** anything is imported into ServiceNow. They are investigation tools: they report, they do not decide. An alert is a reason to look, never a reason to delete or "fix" automatically.

Identifiers and comments inside the scripts are in Portuguese (see decision D14 in [`../docs/decisions.md`](../docs/decisions.md)). The table below describes each script in English.

## Setup

- Python 3.11 (the version used here)
- `pip install -r requirements.txt`
- The data files are not included; see [`data/README.md`](data/README.md)

The scripts find their files through `scripts/caminhos.py`, so they can be run from any folder:

```bash
python scp-api-test/scripts/extrair_titulos_serie1.py
```

## The scripts

| Script | What it does | Writes |
|---|---|---|
| `caminhos.py` | Central place for the project, data and reports paths | nothing |
| `dados.py` | Shared helpers: load the titles, stream the large JSON one record at a time, split a label into its pure title | nothing |
| `extrair_titulos_serie1.py` | Reads the `scp-series` hub from `index.json` and takes each designation from the **link target**, not from the label. Reports ignored links and repeated designations | `data/titulos_serie1.json` |
| `validar_titulos.py` | Checks the extracted titles: empty ones, unusual designations, numbers missing between 1 and 999, and titles marked `N/A` or `[ACCESS DENIED]`. Exits with code 1 when there are problems | nothing |
| `comparar_registros.py` | Compares index designations with the records in the collection; for any missing, searches the other identification fields | nothing |
| `triagem_scp.py` | Flags titles that need a human look (placeholders, `N/A`, access denied) | `reports/relatorio_triagem.csv` |
| `inventariar_midias.py` | Inventories image, audio and video URLs and embedded modules for each record, without downloading anything | `reports/inventario_midias.csv` |
| `buscar_texto_oculto.py` | Finds elements styled with a zero font size. Writes the record, the style and the length of the text, never the text itself | `reports/texto_oculto.csv` |
| `medir_tamanho_conteudo.py` | Prints the articles with the largest `raw_content` | terminal only |
| `contar_mencoes_sites.py` | Counts how many records mention a `Site-N` and which ones are cited most | terminal only |
| `comparar_imagens_fonte.py` | Compares image names declared in the Wikidot source with the API images list and the URL inventory | `diferenca_imagens.csv` |

Typical order: `extrair_titulos_serie1` → `validar_titulos` → `comparar_registros` → `triagem_scp` → `inventariar_midias` → `buscar_texto_oculto`. The two measuring scripts can run at any time.

## What they found

| Result | Value |
|---|---|
| Designations in the Series 1 index | 999 |
| Records in the collection | 984 |
| Index designations without a record | 15 |
| Titles flagged for manual review | 13 |
| Records with image URLs in the API field | 374 |
| Records with audio / video URLs | 6 / 1 |
| Records flagged by the media inventory | 29 |
| Elements with zero-size text | 32, in 5 records |

The story behind these numbers (including how the first extractor lost three titles) is in [`../docs/discoveries.md`](../docs/discoveries.md).

## Principles

- **Nothing is dropped silently.** Anything a script ignores is printed.
- **The original stays untouched.** The scripts only read the source files; derived results go to `data/` and `reports/`.
- **Reports carry no article text.**
- **Alerts are signals, not verdicts.** Absence from the collection does not prove absence from the wiki.

## Known limits

- The hidden-text scan only sees inline `font-size: 0` styles, not CSS classes, `display: none` or matching colours.
- The media inventory covers full `http(s)` URLs and the API `images` field. Files referenced by name only, in the Wikidot source, may be missed.
- The triage list of indicators does not include the `[Blocked]` marker seen on SCP-001.
- The media inventory covers full http(s) URLs and the API images field. Images declared only by file name in the Wikidot source are missed (see comparar_imagens_fonte.py).