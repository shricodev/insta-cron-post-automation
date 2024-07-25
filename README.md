# Insta Cron Post Automation 🐍 ⏰

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![Twitter: shricodev](https://img.shields.io/twitter/follow/shricodev.svg?style=social)](https://twitter.com/shricodev)

![GitHub repo size](https://img.shields.io/github/repo-size/shricodev/insta-cron-post-automation?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/shricodev/insta-cron-post-automation?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/shricodev/insta-cron-post-automation?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/shricodev/insta-cron-post-automation?color=red&style=plastic)

## 📚 Overview

The **Python Insta Post Scheduler** is a Python application designed to automate Instagram posts by scheduling them using **Cronjobs**. This project allows you to post image to Instagram with optional metadata and control various post settings per each post.

## 😎 Features

- **Automated Posting**: Schedule Instagram posts using cron jobs.
- **Flexible Configuration**: Define post details and settings in JSON files.
- **Custom Logging**: Detailed logging of events and errors.
- **Environment Variable Management**: Securely manage Instagram credentials using environment variables.

## ⚠️ Limitations

Since this script uses cron jobs, it will only be able to run the scheduled posts if the scheduled system is up and running. Therefore, it is recommended to run this script in cloud environments in a VM or any environment of your choice. ☁️

## 🌳 Project Structure

```plaintext
insta-cron-post-automation/
├── .git/
├── (gitignored) .venv/
├── data/
│   ├── generated_images/
│   │   ├── .gitkeep
│   │   ├── (gitignored) sample_image_0.jpg
│   │   └── ...
│   ├── scheduled_posts/
│   │   ├── .gitkeep
│   │   ├── (gitignored) insta_post_1cogp9_2024-07-24-11-42.json
│   │   └── ...
│   ├── error.json
│   ├── success.json
│   └── to-post.json
├── logs/
│   ├── .gitkeep
│   └── (gitignored) activity.log
├── src/
│   ├── (gitignored) __pycache__/
│   ├── scripts/
│   │   ├── run_media_post.fish
│   │   └── run_media_post.sh
│   ├── logger_config.py
│   ├── media_post.py
│   ├── populate_sample_posts.py
│   ├── post.py
│   ├── post_list.py
│   └── setup.py
├── (gitignored) .env
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.json
```

## 🛠️ Installation

- **Clone the Repository**

> 💬 If you are using HTTPS protocol instead of SSH, change the `git clone` command accordingly.

```bash
git clone git@github.com:shricodev/insta-cron-post-automation.git
cd insta-cron-post-automation
```

- **Create and Activate Virtual Environment**

```bash
python3 -m venv .venv
source .venv/bin/activate.fish # or .venv/bin/activate if you are not using the fish shell
```

- **Install Dependencies**

```bash
pip3 install -r requirements.json
```

- **Set Up Environment Variables**

```bash
INSTA_USERNAME=<your_instagram_username>
INSTA_PASSWORD=<your_instagram_password>
```

You can use the `.env.example` file as a template.

## 💻 Usage

- **Configure Posts**

Edit the `data/to-post.json` file to include the posts you want to schedule. Ensure each post has the required fields:

```json
{
  "image_path": "path/to/image.jpg",
  "description": "Post description",
  # The post date needs to follow this syntax
  "post_date": "2024-07-06 08:08"
  # Optional
  "extra_data": {
    "custom_accessibility_caption": "Accessibility caption",
    "like_and_view_counts_disabled": 0,
    "disable_comments": 0
  },
}
```

- **Schedule Posts**

Run the `main.py` script to schedule your posts:

```bash
python3 main.py
```

This script will:

- Load posts from the JSON file.
- Creates an individual json file for each post inside the `data/scheduled_posts/` directory.
- Schedule cron jobs to post at the specified times.

## 💬 Logging

The application logs detailed information about events and errors. You can view the logs in the `logs/activity.log` file.
Also, you can view the success and error logs for each post in the `data/success.json` and `data/error.json` files respectively.

## Show your support

Give a ⭐️ if this project helped you!
