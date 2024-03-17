import logging


def log_config():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="../logs/server.log",
        filemode="a",
    )


def log_info(info):
    logging.info(info)


def log_warning(info):
    if info is not None and type(info) == str:
        logging.warning(info)


def log_error(info):
    if info is not None and type(info) == str:
        logging.error(info)
