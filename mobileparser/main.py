# -*- coding: utf-8 -*-

import sys
import logging
from __init__ import __version__
from sodexo import Sodexo
from unica import Unica


def main(argv):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(" {0}".format(__name__))
    unica_parser = Unica()
    sodexo_parser = Sodexo()
    print "Mobileparser version", __version__
    print unica_parser
    print sodexo_parser
    try:
        html = unica_parser.load_page("httpasd://www.unica.fi/fi")
    except Exception, e:
        logger.exception(e)

if __name__ == "__main__":
    main(sys.argv)
