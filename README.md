Instagram-Twitter-AutoPost

📌 Project Overview

Instagram-Twitter-AutoPost is an automation tool that:

Fetches Instagram posts (captions and media).                                                                               

Summarizes the captions using an AI model (BART-large).

Automatically posts the summary to Twitter (X.com).


This project is useful for content creators, businesses, and news agencies to maintain active engagement across platforms with minimal effort.

📁 System Overview & Architecture

The project consists of three main modules:

1️⃣ Instagram Fetching – Retrieves the latest posts from a specified Instagram username.

2️⃣ AI Summarization – Uses BART-large to generate concise summaries.

3️⃣ Twitter Auto-Posting – Posts the summarized content to X.com.

+------------------------------------------------------+
|            Instagram-Twitter-AutoPost               |
+------------------------------------------------------+
|  1. Fetch Instagram Post  |  2. Summarize Caption   |
+------------------------------------------------------+
|      3. Auto-Post Summary to X.com (Optional)       |
+------------------------------------------------------+

🛠 Setup Instructions & Environment Requirements

1️⃣ Installation

Ensure Python (>=3.8) is installed, then install dependencies:

pip install -r requirements.txt


2️⃣ API Keys Configuration

You need API credentials for Instagram and Twitter. Store them in an .env file:

INSTAGRAM_ACCESS_TOKEN=your_instagram_token

TWITTER_API_KEY=your_twitter_key

TWITTER_API_SECRET=your_twitter_secret

TWITTER_ACCESS_TOKEN=your_twitter_access_token

TWITTER_ACCESS_SECRET=your_twitter_access_secret


🖥 Running the Project

Command Line Execution

To fetch and summarize an Instagram post:

python main.py --username bbcnews

To fetch, summarize, and auto-post to Twitter:

python main.py --username bbcnews --autopost

For debugging, enable verbose mode:

python main.py --username bbcnews --debug


📡 API Endpoints & Usage

This project can also run as a web API with the following endpoints:

Endpoint	      Method	        Description

/fetch_instagram_post	GET	Retrieves the latest Instagram post

/summarize_caption	POST	Summarizes a given caption

/post_to_twitter	POST	Posts the summary to X.com

Example API Request

curl -X GET "http://127.0.0.1:5000/fetch_instagram_post?username=bbcnews"



📜 Features

✅ Fetches latest Instagram post

✅ Uses AI for concise, meaningful summaries

✅ Auto-posts summaries to Twitter (X.com)

✅ API support for integration

✅ Modular design for easy customization
