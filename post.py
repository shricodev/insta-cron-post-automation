class Post:
    def __init__(self, description, image_path, post_date, posted):
        self.image_path = image_path
        self.description = description
        self.post_date = post_date
        self.posted = posted

    def serialize(self):
        date = self.post_date.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "image_path": self.image_path,
            "description": self.description,
            "post_date": date,
            "posted": self.posted,
        }
