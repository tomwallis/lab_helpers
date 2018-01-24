#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script to check what name a pressed key has.

Basically duplicates functionality of psychopy/demos/coder/input/what_key.py

Waits for keypress, then prints name of key.

"""

from __future__ import division
from psychopy import visual, event, core

win = visual.Window([800, 600], units='pix')

keys = []
while not keys:
    keys = event.getKeys()

print(keys)
core.quit()
