# Data files (not included)

The two large JSON files the scripts read are **not committed** to this repository. They contain the text of hundreds of wiki articles (CC BY-SA 3.0), so publishing them would mean attributing each page, and they are large. They are listed in `.gitignore`, and the rule exists from the first commit because Git history is permanent.

Small derived files (`titulos_serie1.json` and the CSV reports) are committed. They hold designations, title labels, URLs and counts, never article text. See [`licenses/LICENSES.md`](../../licenses/LICENSES.md).

## Where they come from

The [scp-data](https://github.com/scp-data) project publishes a dataset of SCP articles and metadata, rebuilt regularly by crawling the wiki. Two files from it are used:

| File | What it is | Path to find it
|---|---|---|
| `content_series-1.json` | One record per Series 1 article | [scp-data/scp-api/blob/main/docs/data/scp/items/content_series-1.json](https://github.com/scp-data/scp-api/blob/main/docs/data/scp/items/content_series-1.json)
| `index.json` | The wiki's hub pages as HTML; only the `scp-series` hub is used | [scp-data/scp-api/blob/main/docs/data/scp/hubs/index.json](https://github.com/scp-data/scp-api/blob/main/docs/data/scp/hubs/index.json)

## Where to put them

```text
scp-api-test/data/content_series-1.json
scp-api-test/data/index.json
```

The scripts find them through `scripts/caminhos.py`, so nothing else needs configuring.

## About the snapshot used in this project

Both files carry a file-system date of **22 Oct 2026** and have never been modified. 

The dataset changes over time, so a newer download may give different counts than the ones in [`docs/discoveries.md`](../../docs/discoveries.md). 

## Terms

The dataset's documentation says it is not affiliated with the SCP Wiki or its administrators, and that all wiki content in it is subject to the wiki's license. This repository treats the data accordingly: CC BY-SA 3.0, with attribution to the wiki and, where possible, to each article's author. The crawler repository (scp_crawler) is MIT-licensed.