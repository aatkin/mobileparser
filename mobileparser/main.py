# -*- coding: utf-8 -*-

import sys
import logging
import logging.config
import datetime
from __init__ import __version__
from sodexo import Sodexo
from unica import Unica


def main(argv):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(" {0}".format(__name__))
    dt = datetime.date.today()

    unica_parser = Unica()
    sodexo_parser = Sodexo()
    logger.info("Mobileparser version " + __version__)
    logger.info(unica_parser)
    logger.info(sodexo_parser)
    # data = unica_parser.parse()
    print dt

if __name__ == "__main__":
    main(sys.argv)
