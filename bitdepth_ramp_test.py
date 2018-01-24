#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script to toggle between a low, medium and high bitdepth lumiance ramp.
For testing high bitdepth monitor modes (e.g. ViewPIXX) perceptually.

"""

from __future__ import division
from psychopy import visual, core, event, gui, data
import numpy as np

# setup params.
params = {'lab?': 'n'}
dlg = gui.DlgFromDict(dictionary=params, title='Location')
if dlg.OK is False:
    core.quit()  # user pressed cancel
params['date'] = data.getDateStr()  # add a simple timestamp


# Setup window
if params['lab?'].lower() == 'n':
    win_x = 800
    win_y = 600
    win = visual.Window([win_x, win_y], units='pix')
elif params['lab'].lower() == 'y':
    win = visual.Window(fullscr=False,
                        # fullscr=True,
                        monitor='viewpixx_default')
else:
    raise ValueError('Lab should be either "y" or "n".')

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

# allow to flip between ramps.
k = []
while not k == ['q']:
    k = event.waitKeys(['left', 'down', 'right', 'q'])
    if k == ['left']:
        im.setImage(lo)
        text.setText("6-bit ramp")
        im.draw()
        text.draw()
        win.flip()
    elif k == ['down']:
        im.setImage(med)
        text.setText("8-bit ramp")
        im.draw()
        text.draw()
        win.flip()
    elif k == ['right']:
        im.setImage(hi)
        text.setText("16-bit ramp")
        im.draw()
        text.draw()
        win.flip()

win.close()
core.quit()
