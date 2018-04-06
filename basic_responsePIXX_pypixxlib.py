#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Basic script to check functionality of responsePIXX button box in our lab.

Want to know what the functions return.

The VIEWPIXX functionality here is implemented with the higher-level pypixxlib,
which currently isn't working. See also my script implementing with the
low-level _libdpx...

"""

from pypixxlib.viewpixx import VIEWPixx3D

my_device = VIEWPixx3D()  # Opens and initiates the device
my_device.updateRegisterCache()  # Update the device

b = []
while not b == ['q']:
    b = my_device.din.getValue()

my_device.close()
