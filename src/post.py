from datetime import datetime
from typing import Any, Dict, Optional


class Post:
    """
    Initializes a new instance of the Post class.

    Args:
        description (str): The description for the post.
        image_path (str): The path to the image file.
        post_date (datetime): The date and time of the post.
        extra_data (Any, optional): Additional data for the post. Defaults to None.
    """

    def __init__(
        self,
        description: str,
        image_path: str,
        post_date: datetime,
        extra_data: Optional[Any] = None,
    ):
        self.image_path = image_path
        self.description = description
        self.post_date = post_date
        self.extra_data = extra_data

    def serialize(self) -> Dict[str, any]:
        """
        Serialize the object into a dictionary representation.

        Returns:
            dict: A dictionary containing the serialized data of the object.
                The dictionary has the following keys:
                - "image_path" (str): The path to the image file.
                - "description" (str): The description for the post.
                - "post_date" (datetime): The date and time of the post.
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
