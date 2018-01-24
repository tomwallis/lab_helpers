#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
find the LS100 photometer on linux.

"""


from __future__ import division
from psychopy import core, hardware

phot = hardware.minolta.LS100('ttyUSB0')
if phot.OK:
    print(phot.getLum())
else:
    core.quit()