import logging


class Logger:
    def __new__(cls, *args, **kwargs):
        cls._logger = super().__new__(cls)
        logging.root.setLevel(logging.NOTSET)
        cls._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s: %(message)s"))
        cls._logger.addHandler(handler)
        return cls._logger
