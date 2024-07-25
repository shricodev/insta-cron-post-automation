import json
import logging
import os
import secrets
import string
import sys
from datetime import datetime
from os import environ
from typing import Dict

from dateutil import tz

# Add the src directory to the module search path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from crontab import CronTab

from src import logger_config, post_list


def get_shell_script_to_run(
    user_shell: str, current_dir: str, logger: logging.Logger
) -> str:
    """
    Determine the script to run based on the user's shell.

    Args:
    - user_shell (str): The user's shell.
    - current_dir (str): The current directory of the script.
    - logger (logging.Logger): The logger to use.

    Returns:
    - str: The path to the appropriate shell script for the user's shell.

    Raises:
    - SystemExit: If the user's shell is unsupported.
    """

    shell_script_map: Dict[str, str] = {
        "bash": os.path.join(current_dir, "src", "scripts", "run_media_post.sh"),
        "fish": os.path.join(current_dir, "src", "scripts", "run_media_post.fish"),
    }

    run_media_post_path = shell_script_map.get(user_shell, None)
    if run_media_post_path is None:
        logger.error(f"Unsupported shell: {user_shell}")
        sys.exit(1)

    return run_media_post_path


def validate_post_date(post_date: str, logger: logging.Logger) -> datetime:
    """
    Validate the post date to ensure it is in the future.

    Args:
    - post_date (string): The date and time of the post.
    - logger (logging.Logger): The logger to use.

    Returns:
    - datetime: The validated and parsed datetime object.

    Raises:
    - SystemExit: If the post date is not valid or not in the future.
    """

    # Define the expected format for parsing
    date_format = "%Y-%m-%d %H:%M"

    try:
        # Attempt to parse the post_date string into a datetime object
        parsed_date = datetime.strptime(post_date, date_format)
    except ValueError:
        logger.error(f"Post date '{post_date}' is not in a valid datetime format.")
        sys.exit(1)

    # Check if the parsed date is in the future
    if parsed_date.astimezone(tz.UTC) <= datetime.now(tz=tz.UTC):
        logger.error(f"Post date '{post_date}' is not in the future.")
        sys.exit(1)

    return parsed_date


def create_cron_job(
    cron: CronTab,
    user_shell: str,
    run_media_post_path: str,
    media_post_path: str,
    scheduled_post_file_path: str,
    post_date: datetime,
    logger: logging.Logger,
) -> None:
    """
    Create a cron job for a scheduled post.

    Args:
    - cron (CronTab): The crontab object for the current user.
    - user_shell (str): The user's shell.
    - run_media_post_path (str): The path to the shell script to run.
    - media_post_path (str): The path to the media post script.
    - scheduled_post_file_path (str): The path to the scheduled post file.
    - post_date (datetime): The date and time to run the job.
    - logger (logging.Logger): The logger to use.

    Raises:
    - SystemExit: If the cron job creation fails.
    """
    try:
        job = cron.new(
            command=f"{user_shell} {run_media_post_path} {media_post_path} {scheduled_post_file_path}"
        )
        job.setall(post_date.strftime("%M %H %d %m *"))
    except Exception as e:
        logger.error(f"ERROR: Failed to create cron job: {e}")
        sys.exit(1)


def main() -> None:
    """
    Main function to schedule Instagram posts using cron jobs.

    This function performs the following tasks:
    1. Sets up logging to a file.
    2. Loads a list of posts from a JSON file.
    3. Creates a temporary JSON file for each post to be scheduled.
    4. Schedules a cron job to execute a script for each post at the specified date and time.
    5. Writes the cron jobs to the user's crontab.

    The cron job will execute the script `media_post.py` with the path to the temporary JSON file as an argument.
    """

    # Determine the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define paths for log file and posts JSON file
    log_path = os.path.join(current_dir, "logs", "activity.log")
    to_post_path = os.path.join(current_dir, "data", "to-post.json")
    media_post_path = os.path.join(current_dir, "src", "media_post.py")

    # Initialize logger
    logger = logger_config.get_logger(log_path)

    post_data_dir = os.path.join(current_dir, "data", "scheduled_posts")
    os.makedirs(post_data_dir, exist_ok=True)

    # Initialize PostList object and load posts from JSON file
    posts_list = post_list.PostList(log_path)

    posts_list.get_posts_from_json_file(to_post_path)
    logger.info(f"Number of posts loaded: {len(posts_list.posts)}")

    user_shell = os.path.basename(environ.get("SHELL", "/bin/bash"))
    run_media_post_path = get_shell_script_to_run(user_shell, current_dir, logger)

    # Access the current user's CronTab object.
    cron = CronTab(user=True)

    for post in posts_list.posts:
        # Create a unique identifier for each post file
        unique_id = "".join(
            secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)
        )

        post.post_date = validate_post_date(post_date=post.post_date, logger=logger)

        # Create a unique suffix for the temporary file based on the post date
        post_date_suffix = post.post_date.strftime("%Y-%m-%d-%H-%M")

        scheduled_post_file_path = os.path.join(
            post_data_dir, f"insta_post_{unique_id}_{post_date_suffix}.json"
        )

        # Write the post data to the temporary file
        try:
            with open(scheduled_post_file_path, "w") as f:
                json.dump(post.serialize(), f, default=str)
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to write post file: {e}")
            sys.exit(1)

        # Create a new cron job to run the Instagram post script with the temp file as an argument
        create_cron_job(
            cron=cron,
            user_shell=user_shell,
            run_media_post_path=run_media_post_path,
            media_post_path=media_post_path,
            scheduled_post_file_path=scheduled_post_file_path,
            post_date=post.post_date,
            logger=logger,
        )

    # Write the cron jobs to the user's crontab
    try:
        cron.write()
        logger.info(f"Cronjob added to the CronTab for the current user: {cron.user}")
    except IOError as e:
        logger.error(f"Failed to write to CronTab: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
