---
layout: single
title: Installation
permalink: /en21/installation/
toc: true
toc_stickly: true
sidebar:
  title: "EarthNet2021"
  nav: en21
---

## Installing EarthNet2021 Toolkit

Run
```shell
pip install earthnet
```

For further ways see [here](/en21/tk-overview/).

## Downloading EarthNet2021 Dataset

In `python` run

```python
import earthnet as en

en.Downloader.get(path/to/download/to, splits)
```

For further ways see [here](/en21/ds-download/).

## Installing EarthNet2021 Model Intercomparison Suite

See [here](/en21/mis-installation/).
