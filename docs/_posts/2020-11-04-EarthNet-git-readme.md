---
layout: post
title:  "This is a test: GitLab readme"
date:   2020-11-04 14:04:28 +0100
categories: testing
---
![EarthNet2021: Introductory Art](/assets/images/EarthNet2021_Intro_art.png)

Art generated via neural style transfer over a *blue marble*.

# EarthNet2021: Forecasting High-Resolution Earth Multispectral Imagery.

In this repository lives the overarching framework for EarthNet2021. 
It incorporates as git submodules the 'Dynamic Landscape Adquisition' under `src/datasets` and 'Codyn (pytorch)' and 'Arcon (tensoflow)' under `src/models`. 
It incorporates baseline methods and can spill out all of the plotting and analysis needed for the publication, comparing across models and their ablations, in a end-to-end manner.

### Vision for this repository (Internal) 
This project is to be released together with the NeurIPS 2020 Workshop Dataset/Challenge paper. For that release, the 2 submodules (Arcon and Codyn) will be detached. However, we'll keep working here to generate all of the results we need towards the model publication.

### Resources

- [Doc: Papers Structure and TODO lists](https://docs.google.com/document/d/1AQ4Z9R4UOdM2MvQ1eRSkBjwK1LIH4yoVZ1yGYToMC-4/edit)
- [ShareLatex: EarthNet2021 Paper Draft (NeurIPS 2020 Workshop)](https://sharelatex.gwdg.de/4135679498chkcjrdhsbhx)
- [Tackling Climate Change with ML at NeurIPS2020](https://www.climatechange.ai/events/neurips2020)
- [How to Webinar Tackling Climate Change with ML at NeurIPS2020](https://www.youtube.com/watch?v=prDI7Oy-VMM)

## Setup

1. Clone the repo: `git clone --recursive git@git.bgc-jena.mpg.de:crequ/earthnet2021.git`


> Why `recursive`? Because we have at least one git submodules for hosting models. This means **you'll need to run `git submodule update` when updating your remote.**

2. We recommend setting up a docker container using our [Dockerfile](Dockerfile). Run `docker build . --tag earthnet2021:1.0`

3. Run a Docker container based on the image created. E.g, `docker run -it earthnet2021:1.0`. Use [the util](scripts/docker_run.sh) to run the container attaching properly all havy directories.

4. Run JupyterLab `jupyter lab` port 8888 is forwarded to the one defined in [docker_run.sh](scripts/docker_run.sh)

5. You might just start to work on `hostname:8000`. However, docker/linux might have some bug that induces Jupyter lab irresponsivness due to port forwarding. Try `ssh -N -f -L localhost:8000:localhost:8000 username@hostname `

Submodules, such as 'Arcon' might require to set up a conda environment. If the environment was not created during the Docker build, run `conda create --name ArconSTF36 python=3.6`, then activate the environment `source activate ArconSTF36 `and install the libraries `pip install -r ./src/models/Arcon/requirements.txt `.

## Structure
- **src** contains the submodules for the `datasets` and machine learning `models` . These are git projects themselves. These repositories live in symbiosis inside EarthNet2021. Development can occur on those submodules in the same way it has been done so far. Recent commits on their Master branch will be updated into EarthNet2021.

- **sandbox** contains currently under development functions and pipelines. These might exist only as Jupyter Notebooks playground until full integration.

- **utils** is the place for useful functions that provide visualization, evaluation, npz-to-tfrecods, etc.

- **scripts** is the place for miscelaneous scripts to move data between machines, keep the working environment clean, set up the environments, etc.

- **data** is the place for all of the heavy files. 

  - data/**temp** contains only temporary files. For example data/temp/checkpoints/ will hold images, gifs and tensorboard logs for models during training. But only those models that make the cut will be moved to `pretrained`

  - data/**outputs** holds `/<model_name>/<experiment_name>/<data_split_name>` with  numpy datacubes of the predictions generated over the test set by our trained models. This is the only directory our evaluation pipeline should need to access for inputs.

  - data/**pretrained** has the weights of fully trained and tested models that make their way into the publication.

  - data/**results** our evaluation pipeline should store all relevant figures/tables/animations here.
  
  - data/**datasets** is the directory where we mount `BGI/scratch/vbenson/Landscapes_dynamics/release` (however it will be best to move this content into `scratch/EarthNet2021/data/datasets/` for consistency)

Ideally, `data/` is mounted into the Docker from `BGI/scratch/EarthNet2021/data/` . In any case, utils might contain a script to move the subfolders of the heavy `data/` between Juba/Luga's scratch disk and Minerva's BGI work_2 directory. These heavy folders are included in the .gitignore.

## Running

Your main entry point is run.py.

**configs/** is the location for the submodules configuration files. Each configuration is saved in a .yml format. It defines how to map the arguments given to `run.py` into scripts of each submodules. The config.yml file defines, what script to run, what conda environment, arguments to pass and the experiment_settings.json .

## Our conventions 
### towards an idillic work as a team 
The following is not enforced as we are just two, but would be nice to give a try to follow these practices it's a good oportunity to learn! :D

- Branch names should follow the pattern `<name_description>`. For example, Chris developing a new classication algorithm may name his branch `chris_amazing_classifier`.
- Commit messages should be concise and descriptive; `wip` should be expanded to `wip - simulated annealing test suite`.
- "Commit early and commit often" is good practice. Develop with the mindset of consolidated chunks that can each be described as a unique commit.
- **Pull requests (PRs)**
    - Before requesting review, organize your commits by squashing them w/ [`git rebase -i`](https://medium.com/@slamflipstrom/a-beginners-guide-to-squashing-commits-with-git-rebase-8185cf6e62ec). This is good practice for keeping git history tidy, and signficantly aids your reviewers in looking through the PR; five well-named sequential commits are far easier to review than 23 seeming random commits.
    - Push your feature branch to the mainline (should be `origin`) and open a PR on the repo homepage.
    - Give your PR a descriptive title and briefly describe what you're pushing. If there is useful info to provide the reviewers (e.g. an example noebook to run, a point of entry, or outstanding questions) please include it.
    - In the description tag **one teammates for review**. As this is a two person project, it's pretty obvious who to tag.
    - The reviewer will provide thoughtful feedback, and the developer will address their concerns.
    - All PRs must be signed off by the reviewer before merging into `master`.
    - See the additional PR info below, and the [PR section here](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) for more context.
- git submodule update --remote for updating all submodules

#### Code style

- Follow PEP8
- Docstring follow the sphinx numpy standard:

```
def foobar(x):
    """Is this real life or is this just fantasy?

    Params
    ------
    x : int
        Start index

    Returns
    -------
    y : int
        End index

    """
```
- When in doubt, default to this [Google Python style guide](http://google.github.io/styleguide/pyguide.html).


## Misc.

### More on pull requests

Before each push to the repository, pull request has to be made and sent for review. There are multiple reasons why pull requests are useful. Here are some of them:

- Share the knowledge. With your PR, you are showing to your teammates what is added, for what purpose and how it's implemented
- Learn. Maybe you are used to do the things one way. Your teammates can show you how the things can be done the other way
- Accidental mistakes. There is nothing worse than having stupid typo error in your method or classname, which can then propagate to other modules or classes. Usually additional pair of eyes will catch those
- Consistency. Some of it may be covered with pre hook commit rules and tools like pylint or similar. However, not all can be caught automatically

Pull request should be reviewed and approved by two engineers other than PR author (this is an ideal case. Our team is too small, so let's say only one reviews it). Creating and reviewing pull requests should be part of our standard development process. Some general guidelines for pull requests:

- Write small pull requests. If the feature you are working on is quite large, divide it into smaller pull requests so that its easier to review it
- Commit messages should be short but descriptive. Writing commit messages like "edit" or "change" is really not useful at all
- Once created, review pull request by yourself first. This can help you identify something that needs to be changed or fixed immediately
- Add description for your pull request
- If you want your pull request to be reviewed faster for some reason, don't hesitate to remind your reviewer.
- When merging an approved PR make sure to select Squash and merge. That way we will have a clean git history with one commit per PR.
- Posting pull request link on slack channel can speed up reviewing. Again, have in mind, the shorter your pull request is, less time it will take to review it.

