# -*- coding: utf-8 -*-

import sys
import logging
from __init__ import __version__
from sodexo import Sodexo
from unica import Unica


def main(argv):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(' Mobileparser')
    unica_parser = Unica(logger)
    sodexo_parser = Sodexo(logger)
    print "Mobileparser", __version__
    print unica_parser.name, unica_parser.version
    print sodexo_parser.name, sodexo_parser.version

if __name__ == "__main__":
    main(sys.argv)
