import json
import os
import sys

from .logger_config import get_logger
from .setup import setup_instagrapi


def is_valid_image_extension(file_name):
    valid_extensions = {".jpg", ".jpeg", ".png"}
    return any(file_name.endswith(ext) for ext in valid_extensions)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(current_dir, "logs", "python_insta_post.log")

    logger = get_logger(log_path)

    if len(sys.argv) > 1:
        post_path = sys.argv[1]

        if (not os.path.exists(post_path)) or (not os.path.isfile(post_path)):
            logger.error(f"{post_path} does not exist or is not a file")
            sys.exit(1)

        client = setup_instagrapi(logger)

        with open(post_path, "r") as post_file:
            content = post_file.read()

        json_post_content = json.loads(content)

        if not is_valid_image_extension(json_post_content["image_path"]):
            logger.error(f"{json_post_content['image_path']} is not a valid image")
            sys.exit(1)

        upload_params = {
            "path": json_post_content.get("image_path"),
            "caption": json_post_content.get("description"),
        }

        if "extra_data" in json_post_content:
            # Ensure the data types are correct
            extra_data = json_post_content["extra_data"]
            try:
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
                sys.exit(1)

            # Ensure the values are within the expected range
            extra_data["like_and_view_counts_disabled"] = max(
                0,
                min(1, extra_data["like_and_view_counts_disabled"]),
            )
            extra_data["disable_comments"] = max(
                0, min(1, extra_data["disable_comments"])
            )

            logger.info(f"Posting to Instagram with these extra fields: {extra_data}")

            upload_params["extra_data"] = extra_data

        logger.info("this is the final upload params: ", upload_params)
        upload_media = client.photo_upload(**upload_params)
        logger.info(f"Upload status: {upload_media.model_dump()}")

    else:
        logger.error("No post path provided")
        sys.exit(1)


if __name__ == "__main__":
    main()
