import logging
def setup_logger(name: str, log_file: str, level = logging.INFO):
    """Function to setup a logger; creates a logger that writes to a file.

    Args:
        name (str): Name of the logger.
        log_file (str): File path where the log will be saved.
        level: Logging level (default is logging.INFO).
    """
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger