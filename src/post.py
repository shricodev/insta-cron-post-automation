class Post:
    def __init__(self, description, image_path, post_date, extra_data=None):
        self.image_path = image_path
        self.description = description
        self.post_date = post_date
        self.extra_data = extra_data

    def serialize(self):
        data = {
            "image_path": self.image_path,
            "description": self.description,
            "post_date": self.post_date,
        }

        if self.extra_data:
            data["extra_data"] = self.extra_data

        return data
