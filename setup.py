import os

from dotenv import load_dotenv
from instagrapi import Client


def get_credentials():
    """
    Retrieve the username and password from environment variables.

    This function loads the environment variables from a .env file using dotenv,
    then retrieves the username and password from the environment variables.

    Returns:
    - username (str): The username retrieved from the environment variables.
    - password (str): The password retrieved from the environment variables.

    Raises:
    - Exception: If either the username or password environment variable is missing (None).
    """

    load_dotenv()

    # Get the username and password from the environment variables:
    username = os.getenv("INSTA_USERNAME")
    password = os.getenv("INSTA_PASSWORD")

    # Check if username or password is None, and raise an exception if so.
    if username is None or password is None:
        raise Exception("Username or password environment variable is missing")

    return username, password


def setup_instagrapi():
    """
    Set up the instagrapi client with the provided username and password.

    This function uses the get_credentials() function to retrieve the username and password,
    then initializes the instagrapi client with the credentials.

    Returns:
    - client (instagrapi.Client): The instagrapi client with the provided credentials.

    Raises:
    - Exception: If there is an error logging in to Instagram with the provided credentials.
    """
    username, password = get_credentials()
    client = Client()

    try:
        client.login(username, password)
    except Exception as e:
        raise Exception(f"Error logging in to Instagram: {e}")

    return client
