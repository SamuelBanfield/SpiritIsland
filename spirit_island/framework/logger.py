import logging
import os
from pathlib import Path


class Logger:
    """
    Prints INFO and higher to log_all.log, prints WARNING and higher to the console

    Example usage:

    logger = Logger()

    logger.info("This is an information message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    """

    def __init__(self):
        log_file_path = Path(__file__).resolve().parent.parent / "logs/log_all.log"
        # Create logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # Create file handler and set the logging level to INFO
        file_handler = logging.FileHandler(log_file_path, mode="w")
        file_handler.setLevel(logging.INFO)

        # Create console handler and set the logging level to WARNING
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        file = self.logger.findCaller()
        self.logger.info(f"{message} - {file}")

    def warning(self, message):
        file = self.logger.findCaller()
        self.logger.warning(f"{message} - {file}")

    def error(self, message):
        file = self.logger.findCaller()
        self.logger.error(f"{message} - {file}")


# Make a single logger instance to be passed around the whole project
logger = Logger()
