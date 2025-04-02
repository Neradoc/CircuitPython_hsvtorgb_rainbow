# SPDX-FileCopyrightText: Copyright FastLed https://github.com/FastLED
# SPDX-FileCopyrightText: Copyright 2025 Neradoc, https://neradoc.me
# SPDX-License-Identifier: MIT
"""
`hsvtorgb_rainbow`
================================================================================

Convert an HSV value to RGB using a visually balanced rainbow.


* Author(s): Neradoc

Implementation Notes
--------------------

Ported to python from the FastLed library.
https://github.com/FastLED/FastLED/blob/master/src/hsv2rgb.cpp
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/Neradoc/CircuitPython_hsvtorgb_rainbow.git"

# Yellow has a higher inherent brightness than
# any other color; 'pure' yellow is perceived to
# be 93% as bright as white.  In order to make
# yellow appear the correct relative brightness,
# it has to be rendered brighter than all other
# colors.
# Level Y1 is a moderate boost, the default.
# Level Y2 is a strong boost.
Y1 = 1
Y2 = 0

# G2: Whether to divide all greens by two.
# Depends GREATLY on your particular LEDs
G2 = 0

# Gscale: what to scale green down by.
# Depends GREATLY on your particular LEDs
Gscale = 0


def scale8(i, scale):
    return (i * (1 + scale)) >> 8


def scale8_video(i, scale):
    return (1 if i and scale else 0) + ((i * scale) >> 8)


def hsv2rgb_rainbow(hsv):
    """
    Convert an HSV value to RGB using a visually balanced rainbow.
    This "rainbow" yields better yellow and orange than a straight mathematical "spectrum".
    
    :param Tuple(int, int, int) hsv: Color tuple (hue, saturation, value) as ints 0-255.
    :return Tuple(int, int, int): (red, green, blue) color tuple as ints 0-255.
    """
    hue, sat, val = hsv

    offset = hue & 0x1F  # 0..31

    offset8 = (offset * 8) % 256

    third = scale8(offset8, (256 // 3))  # max = 85

    r, g, b = 0, 0, 0

    if not (hue & 0x80):
        # 0XX
        if not (hue & 0x40):
            # 00X
            # section 0-1
            if not (hue & 0x20):
                # 000
                # case 0: # R -> O
                r = 255 - third
                g = third
                b = 0
            else:
                # 001
                # case 1: # O -> Y
                if Y1:
                    r = 171
                    g = 85 + third
                    b = 0
                if Y2:
                    r = 170 + third
                    twothirds = scale8(offset8, ((256 * 2) // 3))  # max=170
                    g = 85 + twothirds
                    b = 0
        else:
            # 01X
            # section 2-3
            if not (hue & 0x20):
                # 010
                # case 2: # Y -> G
                if Y1:
                    # uint8_t twothirds = (third << 1)
                    twothirds = scale8(offset8, ((256 * 2) // 3))  # max=170
                    r = 171 - twothirds
                    g = 170 + third
                    b = 0
                if Y2:
                    r = 255 - offset8
                    g = 255
                    b = 0
            else:
                # 011
                # case 3: # G -> A
                r = 0
                g = 255 - third
                b = third
    else:
        # section 4-7
        # 1XX
        if not (hue & 0x40):
            # 10X
            if not (hue & 0x20):
                # 100
                # case 4: # A -> B
                r = 0
                # uint8_t twothirds = (third << 1)
                twothirds = scale8(offset8, ((256 * 2) // 3))  # max=170
                g = 171 - twothirds  # 170?
                b = 85 + twothirds

            else:
                # 101
                # case 5: # B -> P
                r = third
                g = 0
                b = 255 - third
        else:
            if not (hue & 0x20):
                # 110
                # case 6: # P -- K
                r = 85 + third
                g = 0
                b = 171 - third

            else:
                # 111
                # case 7: # K -> R
                r = 170 + third
                g = 0
                b = 85 - third

    # This is one of the good places to scale the green down,
    # although the client can scale green down as well.
    if G2:
        g = g >> 1
    if Gscale:
        g = scale8_video(g, Gscale)

    # Scale down colors if we're desaturated at all
    # and add the brightness_floor to r, g, and b.
    if sat != 255:
        if sat == 0:
            r = 255
            b = 255
            g = 255
        else:
            desat = 255 - sat
            desat = scale8_video(desat, desat)
            satscale = 255 - desat
            # satscale = sat # uncomment to revert to pre-2021 saturation behavior

            # nscale8x3_video( r, g, b, sat)
            # brightness_floor = desat
            r = scale8(r, satscale) + desat
            g = scale8(g, satscale) + desat
            b = scale8(b, satscale) + desat

    # Now scale everything down if we're at value < 255.
    if val != 255:

        val = scale8_video(val, val)
        if val == 0:
            r = 0
            g = 0
            b = 0
        else:
            # nscale8x3_video( r, g, b, val)
            r = scale8(r, val)
            g = scale8(g, val)
            b = scale8(b, val)

    return (r, g, b)


def scalef(i, scale):
    return (i * (1 + scale)) / 256


def scalef_video(i, scale):
    return (1 if i and scale else 0) + ((i * scale) / 256)


def rainbow_wheel(hue):
    """
    Convert an hue value to RGB using a visually balanced rainbow.
    This "rainbow" yields better yellow and orange than a straight mathematical "spectrum".
    
    :param float hue: Color hue as a 0.-256. float.
    :return Tuple(int, int, int): (red, green, blue) color tuple as ints 0-255.
    """
    # hue *= 256.

    offset = hue % 32

    offset8 = (offset * 8) % 256

    third = scalef(offset8, (256 / 3))  # max = 85

    r, g, b = 0, 0, 0

    if hue < 0x80:
        # 0XX
        if hue < 0x40:
            # 00X
            # section 0-1
            if hue < 0x20:
                # 000
                # case 0: # R -> O
                r = 255 - third
                g = third
                b = 0
            else:
                # 001
                # case 1: # O -> Y
                if Y1:
                    r = 171
                    g = 85 + third
                    b = 0
                if Y2:
                    r = 170 + third
                    twothirds = scalef(offset8, ((256 * 2) / 3))  # max=170
                    g = 85 + twothirds
                    b = 0
        else:
            # 01X
            # section 2-3
            if hue < 0x60:
                # 010
                # case 2: # Y -> G
                if Y1:
                    # uint8_t twothirds = (third << 1)
                    twothirds = scalef(offset8, ((256 * 2) / 3))  # max=170
                    r = 171 - twothirds
                    g = 170 + third
                    b = 0
                if Y2:
                    r = 255 - offset8
                    g = 255
                    b = 0
            else:
                # 011
                # case 3: # G -> A
                r = 0
                g = 255 - third
                b = third
    else:
        # section 4-7
        # 1XX
        if hue < 0xC0:
            # 10X
            if hue < 0xA0:
                # 100
                # case 4: # A -> B
                r = 0
                # uint8_t twothirds = (third << 1)
                twothirds = scalef(offset8, ((256 * 2) / 3))  # max=170
                g = 171 - twothirds  # 170?
                b = 85 + twothirds

            else:
                # 101
                # case 5: # B -> P
                r = third
                g = 0
                b = 255 - third
        else:
            if hue < 0xE0:
                # 110
                # case 6: # P -- K
                r = 85 + third
                g = 0
                b = 171 - third

            else:
                # 111
                # case 7: # K -> R
                r = 170 + third
                g = 0
                b = 85 - third

    # This is one of the good places to scale the green down,
    # although the client can scale green down as well.
    if G2:
        g = g / 2
    if Gscale:
        g = scalef_video(g, Gscale)

    return (r, g, b)
