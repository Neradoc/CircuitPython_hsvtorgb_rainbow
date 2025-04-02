# SPDX-FileCopyrightText: Copyright 2025 Neradoc, https://neradoc.me
# SPDX-License-Identifier: MIT
"""
A version of the spectrum conversion with uniform brightness.
Uniform brightness means R+G+B is a constant (before applying sat and val)
"""


def hsv2rgb_spectrum(hsv):
    """
    Convert an HSV value to RGB using a spectrum with uniform brightness.

    :param Tuple(int, int, int) hsv: Color tuple (hue, saturation, value) as ints 0-255.
    :return Tuple(int, int, int): (red, green, blue) color tuple as ints 0-255.
    """
    hue, sat, val = hsv

    if hue <= 85:
        r = 256 - hue * 3
        g = hue * 3
        b = 0
    elif hue <= 170:
        r = 0
        g = 256 - (hue - 85) * 3
        b = (hue - 85) * 3
    else:
        r = (hue - 170) * 3
        g = 0
        b = 256 - (hue - 170) * 3

    r, g, b = (int(x * val / 256) for x in (r, g, b))
    r, g, b = (int(x * sat / 256) + (256 - sat) for x in (r, g, b))

    return (r, g, b)
