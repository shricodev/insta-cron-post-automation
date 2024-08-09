import logging
import os
import sys
from typing import NoReturn, Tuple

from dotenv import load_dotenv
from instagrapi import Client


def log_and_exit(logger: logging.Logger, message: str) -> NoReturn:
    """
    Log an error message and exit the program.

    Args:
    - logger (logging.Logger): The logger to use.
    - message (str): The error message to log.
    """
    logger.error(message)
    sys.exit(1)


def get_credentials(logger: logging.Logger) -> Tuple[str, str]:
    """
    Retrieve the username and password from environment variables.

    This function loads the environment variables from a .env file using dotenv,
    then retrieves the username and password from the environment variables.

    Args:
    - logger (logging.Logger): The logger instance to use for logging.

    Returns:
    - Tuple[str, str]: A tuple containing the username and password retrieved from the environment variables.

    Raises:
    - SystemExit: If the username or password environment variable is missing.
    """

    load_dotenv()

    # Get the username and password from the environment variables:
    username: str | None = os.getenv("INSTA_USERNAME")
    password: str | None = os.getenv("INSTA_PASSWORD")

    # Check if username or password is None, and raise an exception if so.
    if username is None or password is None:
        log_and_exit(
            logger=logger,
            message="Username or password environment variable is missing",
        )

    return username, password


def setup_instagrapi(logger: logging.Logger) -> Client:
    """
    Set up the instagrapi client with the provided username and password.

    This function uses the get_credentials() function to retrieve the username and password,
    then initializes the instagrapi client with the credentials.

    Args:
    - logger (logging.Logger): The logger instance to use for logging.

    Returns:
    - client (instagrapi.Client): The instagrapi client with the provided credentials.

    Raises:
    - SystemExit: If an error occurs while logging in to Instagram.
    """
    username, password = get_credentials(logger=logger)
    client = Client()

    try:
        login_success = client.login(username=username, password=password)

        if not login_success:
            log_and_exit(logger=logger, message="Instagram Login failed")

        logger.info("Instagram Login successful")

    except Exception as e:
        log_and_exit(
            logger=logger, message=f"An error occurred while trying to login: {e}"
        )

    return client
