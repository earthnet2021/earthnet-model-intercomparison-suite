![EarthNet2021: Introductory Art](/imgs/EarthNet2021_Intro_art.png)
Art generated via neural style transfer over a *blue marble*.

# EarthNet2021: Forecasting High-Resolution Earth Multispectral Imagery.

In this repository lives the Model Intercomparison Project for EarthNet2021 (ENMIP). 
It incorporates models that have entered the challenge as submodules under `src/models` and the persistance baseline. It can spill out a ton of the plots and analysis across the different test tracks.

### Resources

- [Full documentation on EarthNet Website](https://www.earthnet.tech/docs/quick-start-guide/)
- [EarthNet2021 paper](https://arxiv.org/linktopaper)
- [Video: why predict Earth surface?](https://www.earthnet.tech/docs/why/)
- [EarthNet toolkit on Pypi](https://pypi.org/project/earthnet)

## Setup

1. Clone the repo: `git clone --recursive https://github.com/earthnet2021/earthnet.git`


> Why `recursive`? Because we have git submodules for hosting models. This means **you'll need to run `git submodule update` when updating your remote.**

2. We recommend setting up a docker container using our [Dockerfile](Dockerfile). Run `docker build . --tag earthnet2021:1.0`

3. Run a Docker container based on the image created. E.g, `docker run -it earthnet2021:1.0`. Use [the util](scripts/docker_run.sh) to run the container attaching properly all havy directories.

4. Run JupyterLab `jupyter lab` port 8888 is forwarded to the one defined in [docker_run.sh](scripts/docker_run.sh)

5. You might just start to work on `hostname:8000`. However, docker/linux might have some bug that induces Jupyter lab irresponsivness due to port forwarding. Try `ssh -N -f -L localhost:8000:localhost:8000 username@hostname `

Submodules, such as 'tf_template' might require to set up a conda environment. If the environment was not created during the Docker build, run `conda create --name ENtf115py36 python=3.6`, then activate the environment `source activate ENtf115py36 `and install the libraries `pip install -r ./src/models/tf_template/requirements.txt `.

## Structure
- **src** contains the submodules for the `datasets` and machine learning `models` . These are git projects themselves. These repositories live in symbiosis inside EarthNet2021. Development can occur on those submodules in the same way it has been done so far. Recent commits on their Master branch will be updated into EarthNet2021.

- **utils** is the place for useful functions e.g., npz-to-tfrecods.

- **scripts** is the place for miscelaneous scripts to move data between machines, keep the working environment clean, set up the environments, etc.

- **data** is the place for all of the heavy files. 

  - data/**temp** contains only temporary files. For example data/temp/checkpoints/ can hold images, gifs and tensorboard logs for models during training. But only those models that make the cut will be moved to `pretrained`

  - data/**outputs** holds `/<model_name>/<experiment_name>/<data_split_name>` with  numpy datacubes of the predictions generated over the test set by our trained models. This is the only directory our evaluation pipeline should need to access for inputs.

  - data/**pretrained** has the weights of fully trained and tested models that make their way into the publication.

  - data/**results** our evaluation pipeline should store all relevant figures/tables/animations here.
  
  - data/**datasets** is the directory where we mount `BGI/scratch/vbenson/Landscapes_dynamics/release` (however it will be best to move this content into `scratch/EarthNet2021/data/datasets/` for consistency)

Ideally, `data/` is mounted into the Docker from a large disk as it will get big quickly.

## Running

Your main entry point is run.py.

**configs/** is the location for the submodules configuration files. Each configuration is saved in a .yml format. It defines how to call standalone models added as submodules from `run.py`. The config.yml file defines what script to run, in which conda environment, the arguments to passed and the experiments settings (as JSON) if any.
