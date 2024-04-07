import logging

from setup import setup_instagrapi


def main():
    logging.basicConfig(
        filename="python_insta_post.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %{levelname}s - %(message)s",
    )

    _ = setup_instagrapi()
    logging.info("Woohoo! successfully logged in to Instagram")


if __name__ == "__main__":
    main()
