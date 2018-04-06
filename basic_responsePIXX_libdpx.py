#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Basic script to check functionality of responsePIXX button box in our lab.

Want to know what the functions return.

"""

from pypixxlib import _libdpx as libdpx

# copied from Rebecca Sharman's script ExpConSameDiffExp2.py:
libdpx.DPxOpen()
libdpx.DPxDisableDinStabilize()
libdpx.DPxEnableDinDebounce()
libdpx.DPxEnableDinLogTimetags()
libdpx.DPxEnableDinLogEvents()
libdpx.DPxSetDinDataDir(int("00FF0000", 16))
libdpx.DPxSetDinBuff(int("C00000", 16), int("400000", 16))
libdpx.DPxSetDinDataOut(int("000000", 16))
libdpx.DPxUpdateRegCache()

# Flush Previous
libdpx.DPxSetDinBuff(int("C00000", 16), int("400000", 16))
libdpx.DPxUpdateRegCache()

resp = None
thisResponse = None

while thisResponse is None:
    libdpx.DPxUpdateRegCache()

    resp = libdpx.DPxGetDinValue() & 31

    if resp == 27:  # green
        thisResponse = 1
        print 'green'

    if resp == 30:  # red
        thisResponse = 0
        print 'red'

    libdpx.DPxUpdateRegCache()

libdpx.DPxClose()