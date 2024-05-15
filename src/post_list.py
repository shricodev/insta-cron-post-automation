import json

from dateutil import parser

from .logger_config import get_logger
from .post import Post


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
                    raise ValueError("No 'posts' key found in the json file")

                for post in data["posts"]:
                    if not all(
                        key in post
                        for key in ["description", "image_path", "post_date"]
                    ):
                        raise ValueError("Missing required keys in the post object")

                    post_obj = Post(
                        description=post["description"],
                        image_path=post["image_path"],
                        post_date=parser.parse(post["post_date"]),
                    )
                    self.posts.append(post_obj)

        except FileNotFoundError:
            self.logger.error(f"File not found: {posts_file_path}")

        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON file: {posts_file_path}")

        except ValueError as ve:
            self.logger.error(f"Error parsing the JSON file: {ve}")

        except Exception as e:
            self.logger.error(f"An internal error occurred: {e}")

        return self.posts
