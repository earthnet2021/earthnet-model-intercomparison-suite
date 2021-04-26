---
layout: single
title: Installation
permalink: /docs/installation/
toc: true
toc_stickly: true
sidebar:
  title: "Documentation"
  nav: docs
---

## Installing EarthNet2021 Toolkit

Run
```shell
pip install earthnet
```

For further ways see [here](/docs/tk-overview/).

## Downloading EarthNet2021 Dataset

In `python` run

```python
import earthnet as en

en.Downloader.get(path/to/download/to, splits)
```

For further ways see [here](/docs/ds-download/).

## Installing EarthNet2021 Model Intercomparison Suite

See [here](/docs/mis-installation/).
