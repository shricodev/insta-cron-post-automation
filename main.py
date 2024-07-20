import os
import sys

import json
import secrets
import string
from os import environ

# Add the src directory to the module search path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from crontab import CronTab

from src import logger_config, post_list

def get_shell_script_to_run(user_shell, current_dir, logger):
    """
    Determine the script to run based on the user's shell.

    Args:
    - current_dir (str): The current directory of the script.
    - logger (logging.Logger): The logger to use.

    Returns:
    - str: The path to the appropriate shell script for the user's shell.

    Raises:
    - SystemExit: If the user's shell is unsupported.
    """

    shell_script_map = {
        'bash': os.path.join(current_dir, "src", "scripts", "run_media_post.sh"),
        'fish': os.path.join(current_dir, "src", "scripts", "run_media_post.fish"),
    }

    run_media_post_path = shell_script_map.get(user_shell, None)
    if run_media_post_path is None:
        logger.error(f"Unsupported shell: {user_shell}")
        sys.exit(1)

    return run_media_post_path

def main():
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
    log_path = os.path.join(current_dir, "logs", "python_insta_post.log")
    to_post_path = os.path.join(current_dir, "data", "to-post.json")

    media_post_path = os.path.join(current_dir, "src", "media_post.py")

    post_data_dir = os.path.join(current_dir, "data", "scheduled_posts")
    os.makedirs(post_data_dir, exist_ok=True)

    # Initialize logger
    logger = logger_config.get_logger(log_path)

    # Initialize PostList object and load posts from JSON file
    posts_list = post_list.PostList(log_path)
    posts_list.get_posts_from_json_file(to_post_path)

    logger.info(f"Number of posts loaded: {len(posts_list.posts)}")

    user_shell = os.path.basename(environ.get("SHELL"))
    run_media_post_path = get_shell_script_to_run(user_shell, current_dir, logger)

    # Access the current user's CronTab object.
    cron = CronTab(user=True)

    for post in posts_list.posts:
        # Create a unique identifier for each post file
        unique_id = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))

        # Create a unique suffix for the temporary file based on the post date
        post_date_suffix = post.post_date.strftime("%Y-%m-%d-%H")

        scheduled_post_file_path = os.path.join(post_data_dir, f"insta_post_{unique_id}_{post_date_suffix}.json")

        with open(scheduled_post_file_path, "w") as f:
            json.dump(post.serialize(), f, default=str)

        # Create a new cron job to run the Instagram post script with the temp file as an argument
        # We need to run it as a python module
        job = cron.new(
            command=f"{user_shell} {run_media_post_path} {media_post_path} {scheduled_post_file_path}"
        )

        # Set the cron job to run at the post date and time
        job.setall(post.post_date.strftime("%M %H %d %m *"))

    # Write the cron jobs to the user's crontab
    cron.write()
    logger.info(f"Job added to the CronTab for the current user: {cron.user}")


if __name__ == "__main__":
    main()
