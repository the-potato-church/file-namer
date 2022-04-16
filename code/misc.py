import logging

null_logger = logging.getLogger("nullLogger")
null_logger.addHandler(logging.NullHandler())
