# Lab test scripts

This repository contains experimental scripts for setting up and testing our psychophysics lab during our migration from PTB to PsychoPy.

Eventually I would move these scripts into the [`psyutils` package](https://github.com/tomwallis/PsyUtils).

Our lab runs Ubuntu Linux 16.04 LTS. Hardware is a VIEWPixx 3D monitor and ResponsePIXX button box.

## TODO

* basic monitor calibration (no fancy modes)
* responsePIXX button box working, with precision timing
* high-bitdepth greyscale mode for VIEWPixx, plus calibration
* improve PsychoPy calibration routines.
* Get LS100 working (can't connect under Linux; perhaps because serial-to-usb)

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


#### The `pypixxlib` utilities for VPIXX

VPIXX offer a python library `pypixxlib` for interfacing with their hardware.
We want to use this within (or alongside) psychopy.
To install the `pypixxlib` in our environment:

1. Download VPIXX Software Tools from their website (under Support; may require
a user account). Copy it into the user's home directory.
1. Use pip to install the library into our python environment 
(remember to have it activated first!):

`pip install -U  PATH_TO_TOOLS/VPixx_Software_Tools/pypixxlib/pypixxlib-XXX.tar.gz`

Note that there's also a command line utility `vputil` that can be used to 
do things like update firmware on the device, etc.


#### The "pylink" package for interfacing with the Eyelink.

The package `pylink` is distributed by SR research
for using the Eyelink in Python. It's also
distributed with Standalone PsychoPy, but that won't work for our dev version.

Download the eyelink developers kit from the
[SR support website](https://www.sr-support.com/forum/downloads/eyelink-display-software/45-eyelink-developers-kit-for-mac-os-x-mac-os-x-display-software?15-EyeLink-Developers-Kit-for-Mac-OS-X-(Mac-OS-X-Display-Software)=)
 and follow their prompts.

Because SR research seem to distribute pylink as compiled python (`.pyc`), we
need to add these to the python path to import (needs to be done for *every
session*). First duplicate the compiled version appropriate for
your python version (here 2.7) into a new folder called simply `pylink`.
So this new folder should be nested in `pylink/pylink`. Then:

```python
import sys
sys.path.append('location/of/pylink')  # note to top dir not version specific
import pylink

```

#### The "pylinkwrapper" package for interfacing with the Eyelink.

The `pylink` package is quite low-level and not so simple to use. Enter
`pylinkwrapper`, which offers some nice wrapper functions
for using the `pylink` toolbox more easily. I forked it from its creator
Nick DiQuattro to here: https://github.com/tomwallis/pylinkwrapper

Since it has no `setup.py` we can't install easily with `pip`. We can
recreate the above by setting the system path to know where it is before
import:

```python
import sys
sys.path.append('location/of/pylink')  # note to top dir not version specific
sys.path.append('location/of/pylinkwrapper')  # note should be dir above pylinkwrapper
import pylinkwrapper
```