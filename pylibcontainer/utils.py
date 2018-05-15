from __future__ import print_function
import sys
import math

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class HumanSize(long):
    """ define a size class to allow custom formatting
        Implements a format specifier of S for the size class - which displays a human readable in b, kb, Mb etc
    """
    def __format__(self, fmt):
        if fmt == "" or fmt[-1] != "S":
            if fmt[-1].tolower() in ['b', 'c', 'd', 'o', 'x', 'n', 'e', 'f', 'g', '%']:
                # Numeric format.
                return long(self).__format__(fmt)
            return str(self).__format__(fmt)

        val, text = float(self), ["b ", "Kb", "Mb", "Gb", "Tb", "Pb"]
        if val < 1:
            # Can't take log(0) in any base.
            i, j = 0, 0
        else:
            i = int(math.log(val, 1024)) + 1
            j = val / math.pow(1024, i)
            j, i = (j, i) if j > 0.5 else (j*1024, i-1)
        return ("{0:{1}f}"+text[i]).format(j, fmt[:-1])
