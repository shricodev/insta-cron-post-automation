import logging
import os
import sys
from datetime import datetime, timedelta
from random import choice
from typing import List

import lorem
import numpy as np
from dateutil import tz
from PIL import Image

from logger_config import get_logger
from post import Post
from post_list import PostList

POST_COUNT = 1


def handle_error(logger: logging.Logger, message: str) -> None:
    """
    Log an error message and exit the program.

    Args:
    - logger: The logger instance to use for logging the error.
    - message (str): The error message to log.
    """
    logger.error(message)
    sys.exit(1)


def generate_sample_images(
    num_images: int, width: int, height: int, save_dir: str
) -> List[str]:
    """
    Generate random images and save them to the specified directory.

    Args:
    - num_images (int): Number of images to generate.
    - width (int): Width of the images.
    - height (int): Height of the images.
    - save_dir (str): Directory to save the images.

    Returns:
    - List[str]: List of file paths of the saved images.

    Raises:
    - SystemExit: If any of the input parameters are invalid.
    """
    if num_images <= 0 or width <= 0 or height <= 0:
        handle_error(
            logger, "Invalid input parameters. Please provide positive values."
        )

    # Create the save_dir folder if it does not exist
    os.makedirs(save_dir, exist_ok=True)

    file_paths: List[str] = []

    for i in range(num_images):
        # Generate random pixel data for an image
        random_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

        # Create an image from the pixel data
        image = Image.fromarray(random_data, "RGB")

        image_format = "jpg"
        file_path = os.path.join(save_dir, f"sample_image_{i}.{image_format}")

        try:
            image.save(file_path)
            file_paths.append(file_path)
        except Exception as e:
            handle_error(logger, f"There was a problem saving image {i}: {e}")

    return file_paths


def generate_sample_posts(num_posts: int, image_paths: List[str]) -> List[Post]:
    """
    Generate a list of sample posts.

    Args:
    - num_posts (int): The number of posts to generate.
    - image_paths (List[str]): The list of image paths to use for the posts.

    Returns:
    - List[Post]: A list of Posts

    Raises:
    - SystemExit: If any of the input parameters are invalid.
    """
    if not isinstance(num_posts, int) or num_posts <= 0:
        handle_error(
            logger, "Number of posts must be a positive integer greater than 0."
        )

    if not isinstance(image_paths, list) or not all(
        isinstance(path, str) for path in image_paths
    ):
        handle_error(logger, "Invalid image paths. Please provide a list of strings.")

    posts: List[Post] = []

    for _ in range(num_posts):
        current_time = datetime.now(tz=tz.UTC)

        # Add a few hours and minutes to the current time to ensure the post is in the future
        tomorrow = current_time + timedelta(days=1)

        post_obj = Post(
            image_path=choice(image_paths),
            description=lorem.sentence(),
            post_date=tomorrow.strftime("%Y-%m-%d %H:%M"),
        )
        posts.append(post_obj)
    return posts


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(current_dir, "..", "logs", "activity.log")
    to_post_path = os.path.join(current_dir, "..", "data", "to-post.json")
    sample_images_dir = os.path.join(current_dir, "..", "data", "generated_images")

    logger = get_logger(log_path)

    post_list = PostList(log_path)

    image_paths = generate_sample_images(
        num_images=POST_COUNT, width=1080, height=1340, save_dir=sample_images_dir
    )

    sample_posts = generate_sample_posts(POST_COUNT, image_paths=image_paths)

    post_list.posts.extend(sample_posts)

    try:
        with open(to_post_path, "w") as f:
            f.write(post_list.to_json())
    except Exception as e:
        handle_error(
            logger, f"There was a problem writing sample posts to '{to_post_path}': {e}"
        )

    logger.info(f"Sample posts written to '{to_post_path}'")
