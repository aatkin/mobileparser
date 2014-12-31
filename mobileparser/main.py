# -*- coding: utf-8 -*-

import sys
import logging
import logging.config

from __init__ import __version__
from sodexo import Sodexo
from unica import Unica


def main(argv):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(" {0}".format(__name__))

    logger.info(" Mobileparser version " + __version__)

    parsers = {}
    parsers["unica"] = Unica()
    parsers["sodexo"] = Sodexo()

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in parsers:
            parsers[arg].parse()
        else:
            logger.warning(" No parsers exist for key " + arg)
    else:
        for key, value in parsers.iteritems():
            logger.info(value)

if __name__ == "__main__":
    main(sys.argv)
