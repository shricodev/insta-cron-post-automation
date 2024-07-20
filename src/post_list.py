import json
import sys

from dateutil import parser

from logger_config import get_logger
from post import Post


class PostList:
    """
    A class to manage/represent a list of posts.
    """

    def __init__(self, log_path):
        self.posts = []
        self.logger = get_logger(log_path)

    def serialize(self):
        """
        Serialize the list of posts into a JSON string.
        Use this method to write the content in the `self.posts` array to a JSON file.

        Returns:
            str: JSON string representing the serialized posts.
        """
        serialized_posts = [post.serialize() for post in self.posts]
        return json.dumps({"posts": serialized_posts}, default=str)

    def get_posts_from_json_file(self, posts_file_path):
        """
        Load posts from a JSON file and populate the list.

        Args:
            posts_file_path (str): The path to the JSON file containing post data.

        Returns:
            list: List of Post objects loaded from the JSON file.
        """
        try:
            with open(posts_file_path, "r") as posts_json_file:
                data = json.load(posts_json_file)

                if "posts" not in data:
                    self._handle_error("No 'posts' key found in the json file")

                for post in data["posts"]:
                    if not all(
                        key in post
                        for key in ["image_path", "description", "post_date"]
                    ):
                        self._handle_error("Missing required keys in the post object")

                    extra_data = post.get("extra_data")

                    post_obj = Post(
                        image_path=post["image_path"],
                        description=post["description"],
                        post_date=parser.parse(post["post_date"]),
                        extra_data=extra_data,
                    )
                    self.posts.append(post_obj)

        except FileNotFoundError:
            self._handle_error(f"File not found: {posts_file_path}")

        except PermissionError:
            self._handle_error(f"Permission denied: {posts_file_path}")

        except json.JSONDecodeError:
            self._handle_error(f"Invalid JSON file: {posts_file_path}")

        except ValueError as ve:
            self._handle_error(f"Invalid date format provided in the post object: {ve}")

        except Exception as e:
            self._handle_error(f"Unexpected error: {e}")

        return self.posts

    def _handle_error(self, message):
        """
        Log an error message and exit the program.

        Args:
            message (str): The error message to log.
        """
        self.logger.error(message)
        sys.exit(1)
