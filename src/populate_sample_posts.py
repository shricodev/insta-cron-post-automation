import os
from datetime import datetime
from random import choice

import lorem
import numpy as np
from dateutil import tz
from PIL import Image

from logger_config import get_logger
from post import Post
from post_list import PostList

POST_COUNT = 2
DESCRIPTIONS = [lorem.sentence() for _ in range(POST_COUNT)]


def generate_sample_images(num_images, width, height, save_dir):
    """
    Generate random images and save them to the specified directory.

    Args:
        num_images (int): Number of images to generate.
        width (int): Width of the images.
        height (int): Height of the images.
        save_dir (str): Directory to save the images.

    Returns:
        List[str]: List of file paths of the saved images.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_paths = []

    for i in range(num_images):
        # Generate random pixel data for an image
        random_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

        # Create an image from the pixel data
        image = Image.fromarray(random_data, "RGB")

        file_path = os.path.join(save_dir, f"sample_image_{i}.jpg")

        # Save the image to the specified file path
        image.save(file_path)
        file_paths.append(file_path)

    return file_paths


def generate_sample_posts(num_posts, image_paths):
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
        post_obj = Post(
            image_path=choice(image_paths),
            description=choice(DESCRIPTIONS),
            post_date=datetime.now(tz=tz.UTC).isoformat(),
        )
        posts.append(post_obj)
    return posts


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(current_dir, "..", "logs", "python_insta_post.log")
    to_post_path = os.path.join(current_dir, "..", "data", "to-post.json")

    logger = get_logger(log_path)

    post_list = PostList(log_path)
    image_paths = generate_sample_images(
        num_images=POST_COUNT, width=640, height=480, save_dir="/tmp"
    )

    sample_posts = generate_sample_posts(POST_COUNT, image_paths=image_paths)

    post_list.posts.extend(sample_posts)

    with open(to_post_path, "w") as f:
        f.write(post_list.serialize())

    logger.info(f"Sample posts written to '{to_post_path}'")
