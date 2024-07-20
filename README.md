# Python Insta Post Scheduler 🐍

## Overview

The **Python Insta Post Scheduler** is a Python application designed to automate Instagram posts by scheduling them using cron jobs. This project allows you to post image to Instagram with optional metadata and control various post settings through a configuration file.

## Features

- **Automated Posting**: Schedule Instagram posts using cron jobs.
- **Flexible Configuration**: Define post details and settings in JSON files.
- **Custom Logging**: Detailed logging of events and errors.
- **Environment Variable Management**: Securely manage Instagram credentials using environment variables.

## Limitations

Since this script uses cron jobs, it will only be able to run the scheduled posts if the system is up and running. Therefore, it is recommended to run this script in cloud environments.

## Project Structure

```plaintext
python-insta-post/
├── .git/
├── .venv/
├── data/
│   ├── error.json
│   ├── success.json
│   └── to-post.json
├── logs/
│   └── python_insta_post.log
├── src/
│   ├── __pycache__
│   ├── logger_config.py
│   ├── populate_sample_posts.py
│   ├── post.py
│   ├── post_list.py
│   ├── media_post.py
│   └── setup.py
├── .env
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.json
```

## Installation

- **Clone the Repository**

```bash
git clone git@github.com:shricodev/python-insta-post.git
cd python-insta-post
```

- **Create and Activate Virtual Environment**

```bash
python3 -m venv .venv
source .venv/bin/activate.fish # or .venv/Scripts/activate if you are not using the fish shell
```

- **Install Dependencies**

```bash
pip3 install -r requirements.json
```

- **Set Up Environment Variables**

```bash
INSTA_USERNAME=your_instagram_username
INSTA_PASSWORD=your_instagram_password
```

You can use the `.env.example` file as a template.

## Usage

- **Configure Posts**

Edit the `data/to-post.json` file to include the posts you want to schedule. Ensure each post has the required fields:

```json
{
  "image_path": "path/to/image.jpg",
  "description": "Post description",
  # Optional
  "extra_data": {
    "custom_accessibility_caption": "Accessibility caption",
    "like_and_view_counts_disabled": 0,
    "disable_comments": 0
  },
  "post_date": "2024-07-06T08:08:46.698926+00:00"
}
```

- **Schedule Posts**

Run the `main.py` script to schedule your posts:

```bash
python3 main.py
```

This script will:

- Load posts from the JSON file.
- Create a temporary file for each post.
- Schedule cron jobs to post images at the specified times.

## Logging

The application logs detailed information about events and errors. You can view the logs in the `logs/python_insta_post.log` file.
Also, you can view the success and error logs for each post in the `data/success.json` and `data/error.json` files respectively.
