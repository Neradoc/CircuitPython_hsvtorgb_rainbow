for hue in range(256):
    if not (hue & 0x80):
        # 0XX
        if hue >= 0x80: print(">128", hue)
        if not (hue & 0x40):
            # 00X
            if hue >= 0x40: print(">64", hue)
            if not (hue & 0x20):
                # 000
                if hue >= 0x20: print(">32", hue)
            else:
                # 001
                if hue < 0x20: print("<32", hue)
        else:
            # 01X
            if hue < 0x40: print("<64", hue)
            if not (hue & 0x20):
                # 010
                if hue >= 0x60: print(">96", hue)
            else:
                # 011
                if hue < 0x60: print("<96", hue)
    else:
        # 1XX
        if hue < 0x80: print("<128", hue)
        if not (hue & 0x40):
            # 10X
            if hue >= 0xC0: print(">64", hue)
            if not (hue & 0x20):
                # 100
                if hue >= 0xA0: print(">32", hue)
            else:
                # 101
                if hue < 0xA0: print("<32", hue)
        else:
            if hue < 0xC0: print("<64", hue)
            if not (hue & 0x20):
                # 110
                if hue >= 0xE0: print(">32", hue)
            else:
                # 111
                if hue < 0xE0: print("<32", hue)

