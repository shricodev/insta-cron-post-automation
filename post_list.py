import json
import logging

from dateutil import parser

from post import Post


class PostList:
    """
    A class to manage/represent a list of posts.
    """

    def __init__(self):
        self.posts = []

    def serialize(self):
        """
        Serialize the list of posts into a JSON string.

        Returns:
            str: JSON string representing the serialized posts.
        """
        serialized_posts = [post.serialize() for post in self.posts]
        return json.dumps({"posts": serialized_posts})

    def get_posts_from_json_file(self, posts_file_path):
        """
        Load posts from a JSON file and populate the list.

        Args:
            posts_file_path (str): The path to the JSON file containing post data.

        Returns:
            list: List of Post objects loaded from the JSON file.
        """
        try:
            with open(posts_file_path) as posts_json_file:
                data = json.load(posts_json_file)

                if "posts" not in data:
                    raise ValueError("No 'posts' key found in the json file")

                for post in data["posts"]:
                    if not all(
                        key in post
                        for key in ["description", "image_url", "post_date", "posted"]
                    ):
                        raise ValueError("Missing keys in the post object")

                    post_obj = Post(
                        description=post["description"],
                        image_path=post["image"],
                        post_date=parser.parse(post["post_date"]),
                        posted=post["posted"],
                    )
                    self.posts.append(post_obj)

        except FileNotFoundError:
            logging.error(f"File not found: {posts_file_path}")

        except json.JSONDecodeError:
            logging.error(f"Invalid JSON file: {posts_file_path}")

        except ValueError as ve:
            logging.error(f"Error parsing the JSON file: {ve}")

        except Exception as e:
            logging.error(f"An internal error occurred: {e}")

        return self.posts
