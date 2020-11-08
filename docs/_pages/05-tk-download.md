---
layout: single
title: Toolkit Quick-Start
permalink: /docs/tk-download/
last_modified_at: 2020-11-09
toc: true
toc_stickly: true
sidebar:
  title: "Getting Started"
  nav: docs
---
WIP, to be further developed.

1. Fork the EarthNet2021 working framework repository, initialize a git environment and pull into your local working directory.
2. Connect your model:
..* If you already have a suitable model. Add it as a git submodule under `/src/models/`. You can redirect the base options of run.py by creating a new configuration YAML for your model in `/configs/`

..* If you do not have a suitable model yet, you can develop a new one in a folder under `/src/models/`. You can also opt for working over one of our [templates](/docs/templates/).