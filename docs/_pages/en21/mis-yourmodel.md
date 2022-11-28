---
layout: single
title: Integrate your model
permalink: /en21/mis-yourmodel/
toc: true
toc_stickly: true
sidebar:
  title: "EarthNet2021"
  nav: en21
---


**This section is to be updated and improved**

This is a short version on how it works.

We consider that each model might be a standalone python script.

*1) Optional: preferably, set up a conda environment for your model. You can also add the 'conda create' command to our Dockerfile.
*2) Add a configuration .yml so your stand alone is called correctly. Specify the name of the conda environment it should be run on.
*3) If a extended list of hyperparamenter has to be passed, consider to stack them into a JSON file and add it into "experiments/modelname"
*4) Confirm that your model can be trained and tested by issuing commands to run.py. 

That's it! Thank you for making it easy to everyone to play with a multitude of models!