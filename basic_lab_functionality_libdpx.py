#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function

"""
This script can be used to test the basic hardware functionality we want
to use in our lab:
- ResponsePIXX button box (check timing?)
- VIEWPIXX 3D high-precision luminance mode on a gamma-corrected monitor.
- Eyelink integration

The script displays a luminance ramp, which can be toggled between a 6, 8
and 16-bit mode using the keyboard or button box. The change between 8 and
16 bit will only be visible if the VIEWPIXX is correctly displaying more than
8-bits of greyscale.

The VIEWPIXX functionality here is implemented with the lower-level libdpx.
This code is copied straight from Rebecca Sharman's script ExpConSameDiffExp2
which she shared on the PsychoPy Discus forum.

The eyelink functionality, if selected, will allow
1. calibration
2. display the participant's gaze position on the screen.
3. writing an eye data file.

"""

from __future__ import division
from psychopy import visual, core, event, gui, data, monitors
from pypixxlib import _libdpx as libdpx
import numpy as np

# setup params.
params = {'lab?': 'n',
          'eyetracker?': 'n',
          'highbit?': 'n',
          'responsePIXX?': 'n'}
dlg = gui.DlgFromDict(dictionary=params, title='Location')
if dlg.OK is False:
    core.quit()  # user pressed cancel


# Setup window
if params['lab?'].lower() == 'n':
    win_x = 800
    win_y = 600
    win = visual.Window([win_x, win_y], units='pix')

    # since we're not in the lab, check we're not trying to use
    # any other options:
    if ((params['eyetracker?'].lower() == 'y') or
            (params['highbit?'].lower() == 'y') or
            (params['responsePIXX?'].lower() == 'y')):
        raise ValueError('You asked for hardware but not in the lab!')

    use_dpx = False

elif params['lab'].lower() == 'y':
    mon = monitors.Monitor('viewpixx_dumb_mode')
    win = visual.Window(size=[win_x, win_y],
                        fullscr=False,
                        # fullscr=True,
                        monitor=mon)

    if ((params['highbit?'].lower() == 'y') or
            (params['responsePIXX??'].lower() == 'y')):
        use_dpx = True

else:
    raise ValueError('Lab should be either "y" or "n".')

# enable vpixx stuff:
if use_dpx is True:
    libdpx.DPxOpen()
    libdpx.DPxDisableDinStabilize()
    libdpx.DPxEnableDinDebounce()
    libdpx.DPxEnableDinLogTimetags()
    libdpx.DPxEnableDinLogEvents()
    libdpx.DPxSetDinDataDir(int("00FF0000", 16))
    libdpx.DPxSetDinBuff(int("C00000", 16), int("400000", 16))
    libdpx.DPxSetDinDataOut(int("000000", 16))
    libdpx.DPxUpdateRegCache()

# get real window size. If on Tom's Macbook (retina display), opened
# window is double the size in px as specified.
win_x, win_y = win.size

# Make stimuli

# create a floating point high precision numpy ramp:
xvals = np.linspace(0, 1, win_x)
yvals = np.ones(win_y)  # times two to compensate for retina window.
xv, yv = np.meshgrid(xvals, yvals)


def convert_bits(x, bitdepth):
    """Convert a floating point array to
    values containing lower precision by hacky rounding.
    Floating point input x assumed scaled
    between 0 and 1.
    """
    return np.floor(x * (2**bitdepth - 1))


def rescale(x):
    """ Linearly rescale an input bounded with min zero
    to lie between -1 and 1.

    """
    if x.min() != 0:
        raise ValueError('input should have min zero.')

    x /= x.max()  # max 1
    x *= 2  # max 2
    x -= 1  # range -1, 1

    if x.min() != -1 and x.max() != 1:
        raise Exception

    return x


def convert_array(array, bitdepth):
    x = np.array(array, copy=True)
    x = convert_bits(x, bitdepth)
    x = rescale(x)
    return x


# create copies of the ramp in lower precision:
lo = convert_array(xv, 6)
med = convert_array(xv, 8)
hi = convert_array(xv, 16)

# Setup psychopy stuff.
im = visual.ImageStim(win=win,
                      name='ramp',
                      image=None,
                      size=(win_x, win_y),
                      interpolate=False)

if params['responsePIXX?'].lower() == 'y':
    text = visual.TextStim(win=win,
                           text=["Press left, middle or right button "
                                 "to cycle images."
                                 " Press q on keyboard to quit."
                                 " Press a keyboard key to continue."],
                           pos=(0, 100))
else:
    text = visual.TextStim(win=win,
                           text=["Press left, down or right to cycle images."
                                 " Press q to quit."
                                 " Press a key to continue."],
                           pos=(0, 100))
text.draw()
win.flip()

event.waitKeys()

# set first image.
im.setImage(lo)
text.setText("6-bit ramp")
im.draw()
text.draw()
win.flip()

# flush Previous responses
libdpx.DPxSetDinBuff(int("C00000", 16), int("400000", 16))
libdpx.DPxUpdateRegCache()

# allow to flip between ramps.
k = []
while not k == ['q']:
    k = event.waitKeys(['left', 'down', 'right', 'q'])

    if params['responsePIXX?'].lower() == 'y':
        resp = None
        thisResponse = None
        libdpx.DPxUpdateRegCache()
        resp = libdpx.DPxGetDinValue()&31

        if resp == 27: #green
            thisResponse = 1
            print('green')

        if resp == 30: #red
            thisResponse = 0
            print ('red')

        libdpx.DPxUpdateRegCache()

    if k == ['left']:
        im.setImage(lo)
        text.setText("6-bit ramp")
    elif k == ['down']:
        im.setImage(med)
        text.setText("8-bit ramp")
    elif k == ['right']:
        im.setImage(hi)
        text.setText("16-bit ramp")

    im.draw()
    text.draw()
    win.flip()

if use_dpx is True:
    libdpx.DPxClose()

win.close()
core.quit()
