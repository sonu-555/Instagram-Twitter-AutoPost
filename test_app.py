import pytest
from unittest.mock import patch
from flask import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    return app.test_client()


@patch('app.fetch_latest_instagram_post')
def test_latest_instagram_post(mock_fetch, client):
    """Test fetching the latest Instagram post"""

    # ✅ Ensure mock response structure matches real API response
    mock_fetch.return_value = {
        "caption": "Test caption from Instagram.",  # ✅ Changed from 'original_caption'
        "summarized_caption": "Test summary.",
        "image_url": "https://example.com/test_image.jpg"
    }

    response = client.get("/latest_instagram_post")
    data = response.get_json()

    assert response.status_code == 200
    assert data["original_caption"] == "Test caption from Instagram."  # ✅ Ensure key matches API output


@patch('app.client.create_tweet')
def test_post_to_twitter(mock_tweet, client):
    """Test posting a tweet to Twitter"""

    from unittest.mock import MagicMock  # ✅ Import MagicMock

    # ✅ Mock Twitter API response correctly
    mock_response = MagicMock()
    mock_response.data = {"id": "1234567890123456789"}  # ✅ Correct format

    mock_tweet.return_value = mock_response  # ✅ Assign mock response

    response = client.post("/post_to_twitter", json={"tweet_text": "Test tweet!"})
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Tweet posted successfully!"
    assert data["tweet_id"] == "1234567890123456789"
