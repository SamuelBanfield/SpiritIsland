import logging


class Logger:
    """
    Example usage:

    logger = Logger()

    logger.info("This is an information message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    """

    def __init__(self, main_log_file="logs/log_all.log"):
        logging.basicConfig(
            filename=main_log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.FileHandler(main_log_file, mode="w")

        # Create error logger
        self.logger = logging.getLogger()

    def info(self, message):
        file = self.logger.findCaller()
        self.logger.info(f"{message} - {file}")

    def warning(self, message):
        file = self.logger.findCaller()
        self.logger.warning(f"{message} - {file}")

    def error(self, message):
        file = self.logger.findCaller()
        self.logger.error(f"{message} - {file}")
