# -*- coding: utf-8 -*-

import sys
from __init__ import __version__
from sodexo import Sodexo
from unica import Unica


def main(argv):
    unica_parser = Unica()
    sodexo_parser = Sodexo()
    print "Mobileparser", __version__
    print unica_parser.name, unica_parser.version
    print sodexo_parser.name, sodexo_parser.version

if __name__ == "__main__":
    main(sys.argv)
