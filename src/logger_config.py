import logging


def get_logger(log_file: str) -> logging.Logger :
    """
    Creates and configures a logger to log messages to a specified file.

    This function sets up a logger with an INFO logging level, adds a file handler
    to direct log messages to the specified log file, and applies a specific log
    message format.

    Args:
        log_file (str): The path to the log file where log messages will be saved.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger instance
    logger = logging.getLogger()

    # Set the logging level to INFO
    logger.setLevel(logging.INFO)

    # Create a file handler to write log messages to the specified file
    file_handler = logging.FileHandler(log_file)

    # Define the format for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Set the defined format to the file handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Return the configured logger instance
    return logger
