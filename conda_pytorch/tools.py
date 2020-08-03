import time
import logging
import functools
import contextlib

LOGGER = logging.getLogger("conda-pytorch")


def init_logging(level=logging.INFO):
    logging.basicConfig(level=level)


@contextlib.contextmanager
def timer(logger, prefix):
    start_time = time.time()
    yield
    logger.info(f"{prefix} took {time.time() - start_time:.3f} [s]")


def timed(prefix):
    """Decorator for timing functions"""
    def dec(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            LOGGER.info(prefix)
            with timer(LOGGER, prefix):
                return f(*args, **kwargs)
        return wrapper
    return dec
