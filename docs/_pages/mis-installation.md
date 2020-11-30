---
layout: single
title: Installation
permalink: /docs/mis-installation/
last_modified_at: 2020-11-29
toc: true
toc_stickly: true
sidebar:
  title: "Documentation"
  nav: docs
---
**WIP, to be further developed.**

## Get the EarthNet2021 model intercomparison suite
1. **Fork** the EarthNet2021 framework github repository.
{::nomarkdown}<p style="margin-top: 5px;margin-bottom: 0px"></iframe><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=earthnet2021&repo=earthnet&type=fork&count=true&size=large" frameborder="0" scrolling="0" width="158px" height="30px"></iframe></p>{:/nomarkdown}
2. **clone** your fork into your local working directory.

## Connect your model

2. For a **new model**, create a new folder under `/src/models/`. You can also start developing a model over one of the provided [templates](/docs/mis-templates/).

1. For an **existing model** that already has a repository and stands alone, add it as a git submodule under `/src/models/`. 
```bash
git submodule add https://github.com/user/awesome_model /src/models/awesome_model
```
You can redirect the arguments passed from `run.py` to your stand-alone model by creating a new configuration YAML in `/configs/`. Find a detailed explanation on how to [integrate your model](/docs/mis-yourmodel/). 