#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
find the LS100 photometer on linux.

"""


from psychopy import core
from psychopy.hardware import minolta

phot = minolta.LS100('/dev/ttyUSB0')
if phot.OK:
    print(phot.getLum())
else:
    core.quit()