import os
import sys

from dotenv import load_dotenv
from instagrapi import Client


def get_credentials(logger):
    """
    Retrieve the username and password from environment variables.

    This function loads the environment variables from a .env file using dotenv,
    then retrieves the username and password from the environment variables.

    Returns:
    - username (str): The username retrieved from the environment variables.
    - password (str): The password retrieved from the environment variables.
    """

    load_dotenv()

    # Get the username and password from the environment variables:
    username = os.getenv("INSTA_USERNAME")
    password = os.getenv("INSTA_PASSWORD")

    # Check if username or password is None, and raise an exception if so.
    if username is None or password is None:
        logger.error("Username or password environment variable is missing")
        sys.exit(1)

    return username, password


def setup_instagrapi(logger):
    """
    Set up the instagrapi client with the provided username and password.

    This function uses the get_credentials() function to retrieve the username and password,
    then initializes the instagrapi client with the credentials.

    Returns:
    - client (instagrapi.Client): The instagrapi client with the provided credentials.
    """
    username, password = get_credentials(logger)
    client = Client()

    try:
        login_success = client.login(username, password)

        if not login_success:
            logger.error("Instagram Login failed")
            sys.exit(1)

    except Exception as exception:
        logger.error(f"An error occurred while logging in to Instagram: {exception}")
        sys.exit(1)

    return client
