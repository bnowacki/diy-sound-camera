# diy-sound-camera

### install dependencies

Install and configure [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

```bash
# create new virtual env
conda create -n acoular python=3.12
conda activate acoular

conda install -c acoular acoular
conda install conda-forge::matplotlib
conda install conda-forge::scipy
conda install conda-forge::moviepy
```

not sure if that's all of the dependencies

## To run jupyter notebooks in vs code

press `CTRL` + `SHIFT` + `p` and select `Python: Select Interpreter` next select the conda env you just created (for me it was `Python 3.12.7 ('acoular')`)

## Generate sound localization video from sound and video files

Create `input_data` folder with `audio.wav` and `video.mp4` files

```bash
./run.sh
```
