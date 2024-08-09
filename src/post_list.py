import json
import sys
from datetime import datetime
from typing import List, NoReturn, Optional

from logger_config import get_logger
from post import Post


class PostList:
    """
    A class to manage/represent a list of posts.
    """

    def __init__(self, log_path: str):
        self.posts = []
        self.logger = get_logger(log_path)

    def _log_and_exit(self, message: str) -> NoReturn:
        """
        Log an error message and exit the program.

        Args:
        - message (str): The error message to log.
        """
        self.logger.error(message)
        sys.exit(1)

    def to_json(self) -> str:
        """
        Serialize the list of posts into a JSON string.
        Use this method to write the content in the `self.posts` array to a JSON file.

        Returns:
        - str: JSON string representing the serialized posts.
        """
        serialized_posts = [post.serialize() for post in self.posts]
        return json.dumps({"posts": serialized_posts}, default=str)

    # Custom function to parse the date without seconds
    def parse_post_date(self, post_date: str) -> str:
        """
        Custom function to parse the date without seconds.

        Args:
        - post_date (str): The date string to parse.

        Returns:
        - str: The parsed date string without seconds.
        """
        date_format = "%Y-%m-%d %H:%M"

        # Parse the date
        parsed_date = datetime.strptime(post_date, date_format)

        # Return the date formatted without seconds
        return parsed_date.strftime("%Y-%m-%d %H:%M")

    def get_posts_from_json_file(self, posts_file_path: str) -> List[Post]:
        """
        Load posts from a JSON file and populate the list.

        Args:
        - posts_file_path (str): The path to the JSON file containing post data.

        Returns:
        - List[Post]: List of Post objects loaded from the JSON file.

        Raises:
        - FileNotFoundError: If the JSON file is not found.
        - PermissionError: If the JSON file cannot be accessed.
        - json.JSONDecodeError: If the JSON file is not valid JSON.
        """
        try:
            with open(posts_file_path, "r") as posts_json_file:
                data = json.load(posts_json_file)

                if "posts" not in data:
                    self._log_and_exit(message="No 'posts' key found in the json file")

                for post in data["posts"]:
                    if not all(
                        key in post
                        for key in ["image_path", "description", "post_date"]
                    ):
                        self._log_and_exit(
                            message="Missing required keys in the post object"
                        )

                    extra_data: Optional[dict] = post.get("extra_data")

                    post_obj = Post(
                        image_path=post["image_path"],
                        description=post["description"],
                        post_date=self.parse_post_date(post_date=post["post_date"]),
                        extra_data=extra_data,
                    )
                    self.posts.append(post_obj)

        except FileNotFoundError:
            self._log_and_exit(message=f"File not found: {posts_file_path}")

        except PermissionError:
            self._log_and_exit(message=f"Permission denied: {posts_file_path}")

        except json.JSONDecodeError:
            self._log_and_exit(message=f"Invalid JSON file: {posts_file_path}")

        except ValueError as ve:
            self._log_and_exit(
                message=f"Invalid date format provided in the post object: {ve}"
            )

        except Exception as e:
            self._log_and_exit(message=f"Unexpected error: {e}")

        return self.posts
