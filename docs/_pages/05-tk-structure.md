---
layout: single
title: Toolkit Structure
permalink: /docs/tk-structure/
last_modified_at: 2020-11-08
toc: true
toc_stickly: true
sidebar:
  title: "Getting Started"
  nav: docs
---
**WIP, to be further developed.**


```bash
TODO

EarthNet2021
├── run.py			# Entry point for training/testing/evaluating/plotting
├── data 	# First training sample
|  ├── dataset
|  └── ...
├── iid_test
```

**Why build on top of the EarthNet2021 framework?** By adding your model to the proposed framework via fork, you collaborate to a tidy model intercomparison project. Having a single suite to train/test/evaluate any model that enters the challenge allows for a lot of post-hoc flexibility, benefiting the knowledge extraction from the body of models. In addition, it will make it very easy for any researcher to be able to compare its work with others and build on top of existing models.
{: .notice--info}

