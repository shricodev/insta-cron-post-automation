import json
import os
import sys
import tempfile

from crontab import CronTab

from src.logger_config import get_logger
from src.post_list import PostList


def main():
    """
    Main function to schedule Instagram posts using cron jobs.

    This function performs the following tasks:
    1. Sets up logging to a file.
    2. Loads a list of posts from a JSON file.
    3. Creates a temporary JSON file for each post to be scheduled.
    4. Schedules a cron job to execute a script for each post at the specified date and time.
    5. Writes the cron jobs to the user's crontab.

    The cron job will execute the script `postit.py` with the path to the temporary JSON file as an argument.
    """

    # Determine the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define paths for log file and posts JSON file
    log_path = os.path.join(current_dir, "logs", "python_insta_post.log")
    to_post_path = os.path.join(current_dir, "data", "to-post.json")

    # Initialize logger
    logger = get_logger(log_path)

    # Initialize PostList object and load posts from JSON file
    post_list = PostList(log_path)
    post_list.get_posts_from_json_file(to_post_path)

    logger.info(f"Number of posts loaded: {len(post_list.posts)}")

    # Get the path of the Python executable and the script to run
    python_executable = sys.executable
    insta_post_path = os.path.join(current_dir, "src", "postit.py")

    # Access the current user's CronTab object.
    cron = CronTab(user=True)

    for post in post_list.posts:
        # Create a unique suffix for the temporary file based on the post date
        post_date_suffix = post.post_date.strftime("%Y-%m-%d-%H")

        # Create a temporary file to store the serialized post data
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, prefix="insta_post_", suffix=f"_{post_date_suffix}"
        ) as temp_file:
            # Serialize and dump the post data to the temporary file
            json.dump(post.serialize(), temp_file, default=str)

        # Get the path of the temporary file
        temp_file_path = temp_file.name

        # Create a new cron job to run the Instagram post script with the temp file as an argument
        job = cron.new(
            command=python_executable + f" {insta_post_path} {temp_file_path}"
        )

        # Set the cron job to run at the post date and time
        job.setall(post.post_date.strftime("%M %H %d %m *"))

    # Write the cron jobs to the user's crontab
    cron.write()
    logger.info(f"Job added to the CronTab for the current user: {cron.user}")


if __name__ == "__main__":
    main()
