from typing import Any, Dict, Optional


class Post:
    """
    Initializes a new instance of the Post class.

    Args:
    - description (str): The description for the post.
    - image_path (str): The path to the image file.
    - post_date (str): The date and time of the post.
    - extra_data (Optional[Dict[str, Any]]): Additional data for the post. Defaults to None.
    """

    ALLOWED_EXTRA_DATA_FIELDS = {
        "custom_accessibility_caption",
        "like_and_view_counts_disabled",
        "disable_comments",
    }

    def __init__(
        self,
        description: str,
        image_path: str,
        post_date: str,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        self.image_path = image_path
        self.description = description
        self.post_date = post_date
        self.extra_data = self.validate_extra_data(extra_data=extra_data)

    def validate_extra_data(
        self, extra_data: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Validates and filters the extra_data dictionary to ensure it contains only allowed fields.

        Args:
        - extra_data (Optional[Dict[str, Any]]): The extra data dictionary to validate.

        Returns:
        - Optional[Dict[str, Any]]: The validated extra data dictionary, or None if input is None or invalid.
        """
        if extra_data is None:
            return None

        validated_data = {
            key: extra_data[key]
            for key in extra_data
            if key in self.ALLOWED_EXTRA_DATA_FIELDS
        }

        return validated_data if validated_data else None

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the object into a dictionary representation.

        Returns:
        - dict: A dictionary containing the serialized data of the object.
                The dictionary has the following keys:
                - "image_path" (str): The path to the image file.
                - "description" (str): The description for the post.
                - "post_date" (str): The date and time of the post.
                If the object has extra data, it is added to the dictionary under the key "extra_data".
        """
        data: Dict[str, Any] = {
            "image_path": self.image_path,
            "description": self.description,
            "post_date": self.post_date,
        }

        if self.extra_data is not None:
            data["extra_data"] = self.extra_data

        return data
