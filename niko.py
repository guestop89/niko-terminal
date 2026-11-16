#!/usr/bin/env python3
"""Niko de OneShot : mosaïque ANSI fidèle à la référence, 56 × 56 pixels."""
import shutil
import sys

PALETTE = {'A': (39, 30, 57), 'B': (53, 37, 75), 'C': (60, 61, 149), 'D': (72, 73, 149), 'E': (72, 75, 201), 'F': (77, 46, 86), 'G': (77, 50, 98), 'H': (79, 78, 175), 'I': (80, 51, 102), 'J': (81, 32, 79), 'K': (87, 39, 45), 'L': (99, 109, 221), 'M': (101, 45, 46), 'N': (105, 56, 80), 'O': (106, 77, 107), 'P': (115, 55, 56), 'Q': (125, 63, 64), 'R': (125, 64, 66), 'S': (130, 63, 62), 'T': (149, 78, 80), 'U': (169, 149, 171), 'V': (170, 116, 146), 'W': (186, 105, 105), 'X': (193, 107, 106), 'Y': (197, 138, 137), 'Z': (199, 114, 114), 'a': (213, 182, 86), 'b': (223, 177, 172), 'c': (239, 237, 244), 'd': (250, 212, 15), 'e': (254, 251, 49), 'f': (254, 254, 254)}

PIXELS = (
    '..........bWXXXXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMKKKWWXXX',
    '.........YZXXXWXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZWWWXXXX',
    '.........ZWXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMKPTWXWXXXXXX',
    '........bXWXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMTTTWXXXXXXXX',
    '........WWXXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMMMPWWXXXWXXXXXX',
    '........WWXXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMMKWXXXXXXXXXXXX',
    '.......WWXXXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMKZWXXXXXXXXXXXX',
    '.......WWXXXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMKZXXXXXXXXXXXXX',
    '.......WWXXXXXZMMMMMMMMMMMMMMMMMMMMMMMMMMZWWXXXXXXXXXXXX',
    '......WXXXXXXXZMMMMMMMMMMPWWWWWWWMMMMMMPWXXXXXXXXXXXXXXX',
    '......WXXXXXXXZMMSTTTTTTTTTTTTTTTTTTTTTTWWXXXXXXXXXXXXXX',
    '......WXXXXWXXXMMTWWWWWWWWQQQQQRSWWWWWWWWWWWWXXXXXXXXXXX',
    '......XWXWWWXXXXSRRRRRRRRQQQQQQQQQQQQRRRRXWWXWXXWXXXXXXX',
    '.....WXXXXZWPPPPRRRRRRRRRQQQQQQQQQQQQRRRRPPPXXXXXXXXXXXX',
    '.....ZZZPPPPQQPSQQQQQQQQQQQQQQQQQQQQQQQQQPRRPPPPZXXXXXXX',
    '.....PPPPPQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQPPRPWXXWX',
    '..TTSRRQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQRSSWX',
    'UYRRQQQQQQQQQQQQQQQQRQQQQRQRRQRQRRQQQQQQQQQQQQQQQQQQQQTT',
    'RSPPQQQQQQQQQQQQQQQQRQQQQRQRRQRQRRQQQQQQQQQQQQQQQQQQQQRQ',
    'QQQQQQQQQRQRQQRQQRRRRRRRRRRRRRRRRRRRRQQRQRQQRQRQQQQQQQQQ',
    'RRRRRQRRSSSPSSSSNGGGGGGGGGGGGGGFGGGNPSSSSSSSSSSSSPQQQQQQ',
    'PPRRQSSQGGGGGGGGDDDTCDDDDDDDDDDDDDFFGGGGGGFGFGGGGSSSPPQQ',
    '.....IGDDDDDDDDDDOTTDDDDDDDDDTTODDDDDDDDDDDIGIGGGGGGGGRP',
    '.....IGIDDDDDDDDTTTTDDDDDDDCTTTTTTDDDDDDDDDDDDDGGGGGGGO.',
    '.....GGGDDDDDDDOTSSTCDDDDDDDTTTTTTOODDDDDDDDDDDIFGGGGGG.',
    '.....GGGDDDDDDDNRNNTDDDDDDDDTTTTTTTTDDDDDDDDDDDDFGGGGGG.',
    '.....GGGDDDDDDNNdWNNDDDDDDDDTTTTTNNNNNIDDDDDDDDDDGGGGGG.',
    '.....GGFDDDDDDKfffcNNDDDDDDDTTTRMdAGddWJNTDDDDDDDGGGII..',
    '.....GGFDDDDDDKfffcNNDDDDDDDTTNUfffJddddNNDDDDDDDGGGII..',
    '.....FGffDDDDCdddWNNTNDDDDDCYYOUfffJdddddNDDDDDDIGGGII..',
    'FFFFFcGffHDDDCddeaNNdJYDDDDCYNddddNFdddddJDDDDDDGGGGII..',
    'FBBFFUFUfULDDCeeeaNNeaYVDDDCYNdddeFJedddeaIDDDDDGGGGGGUU',
    'FBBBBBBFcfUDDCeeeaNNeeYYVDDDYRdddeJFeeeeeeJDDDDDGGGGGGGI',
    '.BBBBBBBBcUIDCeeeaNNeeYYYYYCYeeeeeJFeeeeeeCDDDDDGGGGGGGG',
    '...UBBBBBBBGGCeeeaNNeeYYYYYYVeeeeeJFeeeeeeCDDDDFGGGGGGGG',
    '.......BBBFGIBYeeWNJeeYWWYYYYYeeeeJFeeeeeeCDDDDGGGGFGGGG',
    '..........UGGFYYeeeeeWYYYYYYYYeeeeJFeeeeeYCDDDDGGGG.....',
    '........FFFFGFYYYYYYYYYYYYYYYYYYYeeeeeeeYYCDDDIGGIGIIIID',
    '.....UUUBFOUGFYYYYYYYYYYYYYYYYYYYaaaaaaaYYCDDDIGGDIIIIII',
    '.....FFBBFU.GFYYYYYYYYYYYYYYYYYYYYYYYYYYYYCDDDDGFEIIIIGG',
    '..FBBBBBB...GGFYYYYYYYYYWNYYYYYYYYYYYYYYYYDDDHHGGFEEEEFG',
    '..FFBBF...UBGGGFYYYYYYYTWYJYYYYYYYYYYYYYYYCHAAAAIGGGCEE.',
    '.........FFBGGGGcbYYYYYYYYYYYYYYYYYYYYYYbADBAAAAAGGGGI..',
    '........FBFG.GGGcfcEEYYYYYYYYYYYYYYYYSKAADDBACEEEHGGGII.',
    '.......BBBFG.IGcfULEEHHEVYYYYYYYYYTSSSNAAHAHHEEEEEGGGGGO',
    '.......BBBOU.UGfULEEEEEEDOOOOOWWWWTSRKBAAHIEEEEEEEDIGGGI',
    '.......BBFU...IcEEEEEEHHIAAAAANRSSRSRBBAAEEEEEEEEEEIIGGG',
    '.......AB.....GEEEEEEEAAAAAAAAAFSSSSABCEEEEEEEEEEEEEDGIG',
    '..............CEEEEEEAAAAAAAAAAAAAAEEEEEEEEEEEEEEEEEEEFG',
    '..............EEEEEEEEEEEEAAAAAAAEEEEEEEEEEEEEEEEEEEEEE.',
    '.............EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.',
    '................EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE..',
    '................UUUCEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELU..',
    '...................AEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEHU...',
    '...................KEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEENPP..',
    '.................UNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEKMMMM.',
)

W, H = len(PIXELS[0]), len(PIXELS)

SIGNATURE = "-made by AzuRT <3"
HEART = (
    '.rr...rr.',
    'rrhr.rrrr',
    'rhhrrrrrr',
    'rrrrrrrrr',
    '.rrrrrrr.',
    '..rrrrr..',
    '...rrr...',
    '....r....',
)
HEART_COLORS = {'r': (242, 84, 122), 'h': (255, 165, 184)}


def layout_for_terminal():
    columns, lines = shutil.get_terminal_size((80, 40))
    side_width = len(SIGNATURE) + 3
    if columns >= side_width + 15 and lines >= 11:
        return columns, lines, 'side', side_width
    if columns > len(SIGNATURE) and lines >= 12:
        return columns, lines, 'below', 0
    return columns, lines, 'plain', 0


def grid_for_terminal():
    columns, lines, layout, side_width = layout_for_terminal()
    # Conserver les pixels carrés et réserver l'invite ainsi que la signature.
    footer_rows = 6 if layout == 'below' else 0
    limit = min(W, columns - 1 - side_width, 2 * (lines - 5 - footer_rows))
    width = max(0, limit - limit % 2)
    if width < 2:
        return []
    if width == W:
        return PIXELS
    return [''.join(PIXELS[min(H-1, int((y+.5)*H/width))][min(W-1, int((x+.5)*W/width))] for x in range(width)) for y in range(width)]


def pixel_rows(grid, palette):
    output = []
    def ansi(code, key):
        if key == '.': return '\033[39m' if code == 38 else '\033[49m'
        return '\033[%d;2;%d;%d;%dm' % (code, *palette[key])
    for y in range(0, len(grid), 2):
        row = []
        previous = (None, None)
        for x in range(len(grid[0])):
            top = grid[y][x]
            bottom = grid[y+1][x] if y+1 < len(grid) else '.'
            if top != previous[0]: row.append(ansi(38, top))
            if bottom != previous[1]: row.append(ansi(48, bottom))
            row.append(' ' if top == bottom == '.' else '▀')
            previous = (top, bottom)
        output.append(''.join(row)+'\033[0m')
    return output


def render():
    grid = grid_for_terminal()
    if not grid:
        return ''
    columns, lines, layout, _ = layout_for_terminal()
    output = pixel_rows(grid, PALETTE)
    if layout != 'plain':
        heart = pixel_rows(HEART, HEART_COLORS)
        padding = ' ' * ((len(SIGNATURE) - len(HEART[0])) // 2)
        decoration = [padding + row for row in heart]
        decoration += ['', '\033[38;2;255;165;184m' + SIGNATURE + '\033[0m']
        if layout == 'side':
            start = max(0, min(len(output) // 2 - 2, lines - 5 - len(decoration)))
            output += [' ' * len(grid[0])] * max(0, start + len(decoration) - len(output))
            for index, row in enumerate(decoration, start):
                output[index] += '   ' + row
        else:
            indent = ' ' * max(0, min(columns - 1 - len(SIGNATURE), len(grid[0]) - len(SIGNATURE)))
            output += [indent + row for row in decoration]
    return '\n'.join(output)+'\n'

if __name__ == '__main__':
    if '--svg' in sys.argv:
        print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W+22} {H}" width="624" height="448" shape-rendering="crispEdges"><rect width="{W+22}" height="{H}" fill="#181821"/>')
        for y, row in enumerate(PIXELS):
            for x, key in enumerate(row):
                if key != '.':
                    color = ','.join(map(str, PALETTE[key]))
                    print(f'<rect x="{x}" y="{y}" width="1" height="1" fill="rgb({color})"/>')
        for y, row in enumerate(HEART):
            for x, key in enumerate(row):
                if key != '.':
                    color = ','.join(map(str, HEART_COLORS[key]))
                    print(f'<rect x="{W+6+x}" y="{24+y}" width="1" height="1" fill="rgb({color})"/>')
        print(f'<text x="{W+3}" y="36" font-family="monospace" font-size="1.6" fill="#ffa5b8">-made by AzuRT &lt;3</text>')
        print('</svg>')
    else:
        if '--clear' in sys.argv:
            sys.stdout.write('\033[2J\033[H')
        sys.stdout.write(render())
