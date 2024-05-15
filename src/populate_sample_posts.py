import json
import os
from datetime import datetime
from random import choice

from dateutil import tz

from .logger_config import get_logger

descriptions = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
]

image_paths = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg",
    "https://example.com/image5.jpg",
]


def generate_sample_posts(num_posts):
    """
    Generate a list of sample posts.

    Args:
        num_posts (int): The number of posts to generate.

    Returns:
        List[Dict[str, Union[str, datetime]]]: A list of dictionaries, where each dictionary represents a post.
                                              The dictionary contains the following keys:
                                              - "description" (str): Description for the post.
                                              - "image_path" (str): Path to the image file.
                                              - "post_date" (datetime): Date and time of the post.
    """
    posts = []
    for _ in range(num_posts):
        post = {
            "description": choice(descriptions),
            "image_path": choice(image_paths),
            "post_date": datetime.now(tz=tz.UTC).isoformat(),  # ISO 8601 format
        }
        posts.append(post)
    return posts


def write_to_json_file(posts, filename):
    """
    Write the given list of posts to a JSON file.

    Args:
        posts (List[Dict[str, Union[str, datetime]]]): The list of posts to write.
        filename (str): The name of the file to write to.

    Returns:
        None
    """
    with open(filename, "w") as f:
        json.dump({"posts": posts}, f, indent=2)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(current_dir, "logs", "python_insta_post.log")
    to_post_path = os.path.join(current_dir, "data", "to-post.json")

    logger = get_logger(log_path)

    num_posts = 2

    sample_posts = generate_sample_posts(num_posts)

    write_to_json_file(sample_posts, to_post_path)

    logger.info(f"Sample posts written to '{to_post_path}'")
