class Post:
    def __init__(
        self,
        description,
        image_path,
        post_date,
    ):
        self.image_path = image_path
        self.description = description
        self.post_date = post_date

    def serialize(self):
        return {
            "image_path": self.image_path,
            "description": self.description,
            "post_date": self.post_date,
        }

    def post(self):
        pass
