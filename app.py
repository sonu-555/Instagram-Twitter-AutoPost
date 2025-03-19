import tweepy
import os
import html
from flask import Flask, jsonify, request
from instagram_fetcher import fetch_latest_instagram_post
from transformers import BartForConditionalGeneration, BartTokenizer

app = Flask(__name__)

# ✅ Load the BART model for summarization
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# ✅ Twitter API credentials (Replace with actual values)
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAODPzwEAAAAAu4NdRq2EeiY9myZcqYG6%2FuYjT50%3DvG9oVCmatvJxL8e0hKH5wmyOCDkJSUXnTDFfPUF73XiKOyH5Go"
TWITTER_API_KEY = "hhsX6EUiXG8fQKoSaByew6ZS1"
TWITTER_API_SECRET = "D6Tv3JoZVWzZdU4TOhnza2AzU36fGTQfljwTbUndMCtgcm0BQU"
TWITTER_ACCESS_TOKEN = "1900893666434314241-ZLnGiC35TQSdaiUpSEHTH2RZuFH9A7"
TWITTER_ACCESS_SECRET = "Sf9U3renpFXRRYPbVE0kGVWnb8xMvM5mpSb1kBK2zUvAC"

# ✅ Authenticate with Twitter API v2
client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)


def clean_text(text):
    """Fix encoding issues, decode special characters, and format new lines."""
    text = text.encode("utf-8", "ignore").decode("utf-8")  # Ensure proper encoding
    text = html.unescape(text)  # Decode HTML entities (e.g., &amp; → &)
    text = text.replace("\\n", "\n")  # Fix new line issues
    return text.strip()  # Remove extra spaces


def summarize_caption(caption):
    """Generate a concise summary of the given caption using BART."""
    try:
        inputs = tokenizer("summarize: " + caption, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(inputs.input_ids, max_length=50, min_length=10, length_penalty=2.0, num_beams=4, early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error summarizing caption: {e}"


@app.route('/latest_instagram_post', methods=['GET'])
def get_latest_instagram_post():
    """Fetch and summarize the latest Instagram post for a given username."""
    username = request.args.get('username', 'bbcnews')
    post = fetch_latest_instagram_post(username)

    if not post or post["caption"] == "No caption found":
        return jsonify({"error": "Failed to fetch post"}), 500

    # ✅ Clean and summarize the caption
    original_caption = clean_text(post["caption"])
    summarized_caption = summarize_caption(original_caption)

    return jsonify({
        "original_caption": original_caption.replace("\n", " "),  # Ensures new lines display properly
        "summarized_caption": summarized_caption.replace("\n", " "),  # Ensures new lines display properly
        "image_url": post["image_url"]
    })

@app.route('/post_to_twitter', methods=['POST'])
def post_tweet():
    """Post a tweet using the provided text."""
    try:
        data = request.get_json()

        if not data or "tweet_text" not in data or not data["tweet_text"].strip():
            return jsonify({"error": "Invalid or missing 'tweet_text'"}), 400

        tweet_text = data["tweet_text"].strip()

        # ✅ Post tweet to Twitter API
        response = client.create_tweet(text=tweet_text)

        return jsonify({"message": "Tweet posted successfully!", "tweet_id": response.data["id"]})

    except Exception as e:
        return jsonify({"error": f"Failed to post tweet: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
