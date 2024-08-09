import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, NoReturn, Optional

from instagrapi import Client

from logger_config import get_logger
from setup import setup_instagrapi


def log_and_exit(logger: logging.Logger, message: str) -> NoReturn:
    """
    Log an error message and exit the program.

    Args:
    - logger (logging.Logger): The logger to use.
    - message (str): The error message to log.
    """
    logger.error(message)
    sys.exit(1)


def is_valid_image_extension(file_name: str) -> bool:
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


def handle_post_update(
    success: bool, json_post_content: Dict[str, Any], logger: logging.Logger
) -> None:
    """
    Update the post error file based on the success of the upload.

    Args:
    - success (bool): True if the upload was successful, False otherwise.
    - json_post_content (dict): The content of the post.

    Returns:
    - Return the content of the post file if the read is successful; otherwise, return the default value if provided, or None.
    """

    def load_json_file(file_path: str, default: Optional[Any] = None) -> Any:
        """Helper function to load JSON data from a file."""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    return json.load(file)
            except Exception:
                log_and_exit(
                    logger=logger, message=f"Failed to load post file: {file_path}"
                )

        return default if default is not None else []

    def write_json_file(file_path: str, posts: List[Dict[str, Any]]) -> None:
        """Helper function to save JSON data to a file."""
        for post in posts:
            if "post_date" in post:
                try:
                    post_date = datetime.strptime(
                        post["post_date"], "%Y-%m-%d %H:%M:%S"
                    )
                    post["post_date"] = post_date.strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    post_date = datetime.strptime(post["post_date"], "%Y-%m-%d %H:%M")
                    post["post_date"] = post_date.strftime("%Y-%m-%d %H:%M")
                except Exception as e:
                    log_and_exit(
                        logger=logger, message=f"Failed to parse post date: {e}"
                    )

        try:
            with open(file_path, "w") as file:
                json.dump(posts, file, indent=2)
            logger.info(f"Post file updated: {file_path}")

        except (IOError, json.JSONDecodeError) as e:
            log_and_exit(logger=logger, message=f"Failed to write post file: {e}")

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the directory where the data files are located
    data_dir = os.path.join(current_dir, "..", "data")

    # Define paths to the success, error, and to-post files
    success_file = os.path.join(data_dir, "success.json")
    error_file = os.path.join(data_dir, "error.json")
    to_post_file = os.path.join(data_dir, "to-post.json")

    # Load the current 'to-post' data if it exists, otherwise initialize an empty list
    to_post_data = load_json_file(file_path=to_post_file, default={"posts": []})

    # Determine which file to write to based on the success of the upload
    target_file = success_file if success else error_file

    # Load the current content of the target file if it exists, otherwise initialize an empty list
    target_data = load_json_file(file_path=target_file, default=[])

    # Append the current post content to the target data
    target_data.append(json_post_content)

    # Write the updated target data back to the target file
    write_json_file(file_path=target_file, posts=target_data)

    user_posts = to_post_data["posts"]

    # Filter the posted post from the 'to-post' data
    if any(post == json_post_content for post in user_posts):
        user_posts = [item for item in user_posts if item != json_post_content]
        to_post_data["posts"] = user_posts
        write_json_file(file_path=to_post_file, posts=to_post_data)


def parse_post_file_to_json(post_path: str, logger: logging.Logger) -> Dict[str, Any]:
    """
    Parses the content of a post file into a JSON dictionary.

    Args:
    - post_path (str): The path to the post file.
    - logger (logging.Logger): The logger instance to use for logging errors.

    Returns:
    - Dict[str, Any]: The content of the post file parsed as a JSON dictionary.

    Raises:
    - SystemExit: Exits the program with an error status if the file does not exist,
                  if permission is denied, if JSON decoding fails, or if any other
                  exception occurs during file reading.
    """
    try:
        with open(post_path, "r") as post_file:
            content = post_file.read()
        return json.loads(content)

    except FileNotFoundError:
        log_and_exit(logger=logger, message=f"Post file '{post_path}' does not exist")

    except PermissionError:
        log_and_exit(
            logger=logger,
            message=f"Permission denied when trying to access post file '{post_path}'",
        )

    except json.JSONDecodeError:
        log_and_exit(
            logger=logger, message=f"Failed to decode JSON from post file '{post_path}'"
        )

    except Exception as e:
        log_and_exit(
            logger=logger, message=f"Failed to read post file '{post_path}': {e}"
        )


def handle_post_error(
    error_message: str, json_post_content: Dict[str, Any], logger: logging.Logger
) -> None:
    """
    This function logs an error message, updates the post files to indicate failure,
    and terminates the program with an exit status of 1.

    Args:
    - error_message (str): The error message to be logged.
    - json_post_content (Dict[str, Any]): The content of the post file in JSON format.
    - logger (logging.Logger): The logger instance to use for logging the error.

    Returns:
    - None

    Raises:
    - SystemExit: The program will exit with an exit status of 1.
    """
    handle_post_update(
        success=False, json_post_content=json_post_content, logger=logger
    )
    log_and_exit(logger=logger, message=error_message)


def prepare_upload_params(
    json_post_content: Dict[str, Any], logger: logging.Logger
) -> Dict[str, Any]:
    # Initial needed upload parameters
    upload_params = {
        "path": json_post_content.get("image_path"),
        "caption": json_post_content.get("description"),
    }

    # If the optional field is provided
    if "extra_data" in json_post_content:
        extra_data = json_post_content["extra_data"]
        try:
            extra_data["custom_accessibility_caption"] = str(
                extra_data.get("custom_accessibility_caption", "")
            )
            extra_data["like_and_view_counts_disabled"] = int(
                extra_data.get("like_and_view_counts_disabled", 0)
            )
            extra_data["disable_comments"] = int(extra_data.get("disable_comments", 0))

        except (ValueError, TypeError):
            handle_post_error(
                error_message=f"Failed to parse 'extra_data' field: {json_post_content}",
                json_post_content=json_post_content,
                logger=logger,
            )

        extra_data["like_and_view_counts_disabled"] = max(
            0, min(1, extra_data["like_and_view_counts_disabled"])
        )
        extra_data["disable_comments"] = max(0, min(1, extra_data["disable_comments"]))
        upload_params["extra_data"] = extra_data

    return upload_params


def upload_to_instagram(
    client: Client,
    upload_params: Dict[str, Any],
    json_post_content: Dict[str, Any],
    logger: logging.Logger,
) -> None:
    """
    Uploads media to Instagram and handles logging and updating post files based on the result.

    Args:
    - client: The Instagram client used for uploading media.
    - upload_params (Dict[str, Any]): The parameters for the media upload.
    - json_post_content (Dict[str, Any]): The content of the post file in JSON format.
    - logger (logging.Logger): The logger instance to use for logging errors and success messages.

    Returns:
    - None

    Raises:
    - SystemExit: Exits the program with an error status if the upload fails.
    """
    try:
        # Upload the media to Instagram
        upload_media = client.photo_upload(**upload_params)

        # Get the uploaded post ID
        uploaded_post_id = upload_media.model_dump().get("id", None)
        logger.info(
            f"Successfully uploaded the post on Instagram. ID: {uploaded_post_id}"
        )
        handle_post_update(
            success=True, json_post_content=json_post_content, logger=logger
        )
    except Exception as e:
        handle_post_error(
            error_message=f"Failed to upload the post: {e}",
            json_post_content=json_post_content,
            logger=logger,
        )


def main() -> None:
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
    log_path = os.path.join(current_dir, "..", "logs", "post-activity.log")
    logger = get_logger(log_file=log_path)

    if len(sys.argv) > 1:
        post_path = sys.argv[1]

        # Set up the instagrapi client
        client = setup_instagrapi(logger=logger)

        json_post_content: Dict[str, Any] = parse_post_file_to_json(
            post_path=post_path, logger=logger
        )

        # If the path does not exist or the path is not a file
        if (not os.path.exists(post_path)) or (not os.path.isfile(post_path)):
            return handle_post_error(
                error_message=f"'{post_path}' does not exist or is not a file",
                json_post_content=json_post_content,
                logger=logger,
            )

        image_path = json_post_content["image_path"]

        # Validate image file extension
        if not is_valid_image_extension(image_path):
            return handle_post_error(
                error_message=f"'{image_path}' is not a valid image",
                json_post_content=json_post_content,
                logger=logger,
            )

        upload_params: Dict[str, Any] = prepare_upload_params(
            json_post_content=json_post_content, logger=logger
        )

        # Log the final upload parameters
        logger.info(f"Posting to Instagram with the following details: {upload_params}")

        upload_to_instagram(
            client=client,
            upload_params=upload_params,
            json_post_content=json_post_content,
            logger=logger,
        )

    else:
        log_and_exit(logger=logger, message="Please provide the path to the post file")


if __name__ == "__main__":
    main()
