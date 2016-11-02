import logging
import sys


class BaseMeasureInfo:
    _DEFAULT_FMT = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger(__name__)
    OUT_MSG = ""
    WAVELENGTH = ""
    TIMEOUT_SECONDS_MEASURE = 0

    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            stream=sys.stdout,
            format=self._DEFAULT_FMT)