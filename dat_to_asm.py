#!/usr/bin/env python3
"""Write an ICU data package as the assembly file that `genccode -a gcc` produces.

Usage: dat_to_asm.py <in.dat> <out.S> <little|big>

`genccode` reads the package as 32-bit words in the byte order of the machine it runs on, so it
only produces a correct file for a target of the same endianness. This script writes the words
in the byte order of the target instead, which allows generating the big-endian file anywhere.
"""
import struct
import sys

src, dst, endian = sys.argv[1], sys.argv[2], sys.argv[3]
data = open(src, "rb").read()
data += b"\0" * ((-len(data)) % 4)
words = struct.unpack(("<" if endian == "little" else ">") + "%dI" % (len(data) // 4), data)

HEADER = """.globl icudt78_dat
\t.section .note.GNU-stack,"",%progbits
#ifdef __CET__
# include <cet.h>
#endif
\t.section .rodata
\t.balign 16
#ifdef U_HIDE_DATA_SYMBOL
\t.hidden icudt78_dat
#endif
\t.type icudt78_dat,%object
icudt78_dat:

"""


def fmt(w):
    if w < 10:
        return str(w)
    h = "%X" % w
    return "0x" + ("0" + h if len(h) % 2 else h)


with open(dst, "w") as out:
    out.write(HEADER)
    for i in range(0, len(words), 32):
        out.write(".long " + ",".join(fmt(w) for w in words[i:i + 32]) + "\n")
    out.write(".size icudt78_dat, .-icudt78_dat\n")
