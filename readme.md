# Lab test scripts

This repository contains experimental scripts for setting up and testing our psychophysics lab during our migration from PTB to PsychoPy.

Eventually I would move these scripts into the [`psyutils` package](https://github.com/tomwallis/PsyUtils).

Our lab runs Ubuntu Linux 16.04 LTS. Hardware is a VIEWPixx 3D monitor and ResponsePIXX button box.

## TODO

* basic monitor calibration (no fancy modes)
* responsePIXX button box working, with precision timing
* high-bitdepth greyscale mode for VIEWPixx, plus calibration
* improve PsychoPy calibration routines.

## Notes

VPIXX offer the python wrapper library `pypixxlib`, available from their support page as part of the VPIXX software tools package (may require a user account).
Using that library as standalone seems pretty straightforward (see below), but I'm not yet sure how best to integrate this with PsychoPy.

### A guide to installing a development environment for PsychoPy using conda.

To create a development environment for PsychoPy, in case we want to contribute code to that directly, follow these steps.

We will use `conda` environments to maintain our PsychoPy development version. Install and configure [miniconda](https://conda.io/miniconda.html) if required.

#### New conda environment

`conda create --name psychopy-dev python=2.7 wxpython pyQt`

Activate this environment with

`source activate psychopy-dev`

#### Installing `pyo` **not currently done**

Apparently PsychoPy requires an audio package called  `pyo`. Unfortunately it's not available on `conda` or `pip`, so the easiest way seems to be to download a binary from [here](http://ajaxsoundstudio.com/software/pyo/) and then install into your environment manually. I haven't figured out a way to do this for a specific environment, so I've not done it for now. Seems to still allow basic functionality.


#### Forking psychopy

1. If required, fork the PsychoPy repository from Github and then clone locally. I have a fork [here](https://github.com/tomwallis/psychopy).
2. For this doc, I'll assume your clone of PsychoPy is located at /home/psychopy/
3. PsychoPy has a lot of [dependencies](http://www.psychopy.org/installation.html#dependencies). I think most of them can get taken care of manually if you install into the environment above with `pip`:

` source activate psychopy-dev`

`pip install -e home/psychopy/`

`pip install -r home/psychopy/requirements_dev.txt`

Once this completes you can hopefully run PsychoPy by starting a python session and typing `import psychopy`. At least, I seem to be able to do that and it doesn't raise an error.

Similarly, I can get a Gabor to display here:

`python home/psychopy/psychopy/demos/coder/stimuli/gabor.py `

and edits that I make to that code appear in the display.

Yay?

#### Running tests

It's not yet clear to me how the PsychoPy tests run.
Their docs have the below lines:

`cd home/psychopy/psychopy/tests/`
`./run.py path/to/file_with_doctests.py`

... but I'm not sure what they want me to run with that.