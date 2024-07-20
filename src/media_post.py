import json
import os
import sys

from logger_config import get_logger
from setup import setup_instagrapi


def is_valid_image_extension(file_name):
    """
    Check if the given file name has a valid image extension.

    Valid extensions are: .jpg, .jpeg, .png.

    Args:
    - file_name (str): The name of the file to check.

    Returns:
    - bool: True if the file has a valid image extension, False otherwise.
    """
    valid_extensions = {".jpg", ".jpeg", ".png"}
    return any(file_name.endswith(ext) for ext in valid_extensions)


def update_post_files(success, json_post_content):
    """
    Update the post error file based on the success of the upload.

    Args:
    - json_post_content (dict): The content of the post.
    """

    def load_json_file(file_path, default=None):
        """Helper function to load JSON data from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return default if default is not None else []

    def write_json_file(file_path, data):
        """Helper function to save JSON data to a file."""
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the directory where the data files are located
    data_dir = os.path.join(current_dir, "..", "data")

    # Define paths to the success, error, and to-post files
    success_file = os.path.join(data_dir, "success.json")
    error_file = os.path.join(data_dir, "error.json")
    to_post_file = os.path.join(data_dir, "to-post.json")

    # Load the current 'to-post' data if it exists, otherwise initialize an empty list
    to_post_data = load_json_file(to_post_file, {"posts": []})

    # Determine which file to write to based on the success of the upload
    target_file = success_file if success else error_file

    # Load the current content of the target file if it exists, otherwise initialize an empty list
    target_data = load_json_file(target_file, [])

    # Append the current post content to the target data
    target_data.append(json_post_content)

    # Write the updated target data back to the target file
    write_json_file(target_file, target_data)

    # Filter the posted post from the 'to-post' data
    if any(post == json_post_content for post in to_post_data["posts"]):
        to_post_data["posts"] = [item for item in to_post_data["posts"] if item != json_post_content]
        write_json_file(to_post_file, to_post_data)


def main():
    """
    Main function to handle the posting process.

    - Sets up logging.
    - Checks if a post file path is provided and valid.
    - Reads and parses the post file.
    - Validates the image file extension.
    - Prepares upload parameters.
    - Logs the upload parameters and response.
    """

    # Get the current directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the log file, assuming 'logs' is one level up from the current directory
    log_path = os.path.join(current_dir, "..", "logs", "python_insta_post.log")
    logger = get_logger(log_path)

    if len(sys.argv) > 1:
        post_path = sys.argv[1]

        # Set up the instagrapi client
        client = setup_instagrapi(logger)

        # Read and parse the post file
        with open(post_path, "r") as post_file:
            content = post_file.read()

        json_post_content = json.loads(content)

        if (not os.path.exists(post_path)) or (not os.path.isfile(post_path)):
            logger.error(f"'{post_path}' does not exist or is not a file")
            update_post_files(success=False, json_post_content=json_post_content)
            sys.exit(1)

        # Validate image file extension
        if not is_valid_image_extension(json_post_content["image_path"]):
            logger.error(f"'{json_post_content['image_path']}' is not a valid image")
            update_post_files(success=False, json_post_content=json_post_content)
            sys.exit(1)

        # Prepare upload parameters
        upload_params = {
            "path": json_post_content.get("image_path"),
            "caption": json_post_content.get("description"),
        }

        if "extra_data" in json_post_content:
            extra_data = json_post_content["extra_data"]
            try:
                # Ensure the data types are correct
                extra_data["custom_accessibility_caption"] = str(
                    extra_data.get("custom_accessibility_caption", "")
                )
                extra_data["like_and_view_counts_disabled"] = int(
                    extra_data.get("like_and_view_counts_disabled", 0)
                )
                extra_data["disable_comments"] = int(
                    extra_data.get("disable_comments", 0)
                )

            except (ValueError, TypeError):
                logger.error(
                    f"The 'extra_data' field in the post file is not in the expected format: {json_post_content}"
                )
                update_post_files(success=False, json_post_content=json_post_content)
                sys.exit(1)

            # Ensure the values are within the expected range
            extra_data["like_and_view_counts_disabled"] = max(
                0,
                min(1, extra_data["like_and_view_counts_disabled"]),
            )
            extra_data["disable_comments"] = max(
                0, min(1, extra_data["disable_comments"])
            )

            upload_params["extra_data"] = extra_data

        # Log the final upload parameters
        logger.info(
            f"Posting to Instagram with the following details: {upload_params}",
        )

        try:
            # Upload the media to Instagram
            upload_media = client.photo_upload(**upload_params)

            # Log the upload response
            logger.info(f"Upload response: {upload_media.model_dump()}")

            update_post_files(success=True, json_post_content=json_post_content)
        except Exception as e:
            logger.error(f"Failed to upload the post: {e}")
            update_post_files(success=False, json_post_content=json_post_content)

    else:
        logger.error("No path to the post file was provided")
        sys.exit(1)


if __name__ == "__main__":
    main()
