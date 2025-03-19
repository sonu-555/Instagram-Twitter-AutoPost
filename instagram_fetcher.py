import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_latest_instagram_post(username="bbcnews"):
    """Fetches the latest Instagram post's caption and image URL."""
    try:
        # Set up Selenium
        # Set up Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Runs in background
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        # Start ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)  # Increased timeout

        # Open Instagram profile
        url = f"https://www.instagram.com/{username}/"
        driver.get(url)

        # Scroll multiple times to load posts
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Give time for posts to load

        # Wait for the first post to be visible
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//article//img"))
        )

        # Extract HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract only the first post caption
        captions = soup.select("article span")  # Select all <span> inside posts
        caption = "No caption found"

        for cap in captions:
            if len(cap.text.strip()) > 10:  # Ensure it's not empty or too short
                caption = cap.text.strip()
                break  # Stop after finding the first caption

        # Extract only the first post's image URL
        post_images = soup.select("article img")

        if post_images:
            image_url = post_images[0]["src"]  # Select first image from the first post
        else:
            image_url = "No image found"

        driver.quit()

        return {"caption": caption, "image_url": image_url}

    except Exception as e:
        logging.error(f"Error fetching Instagram post: {e}")
        return None

# Test script
if __name__ == "__main__":
    post = fetch_latest_instagram_post()
    if post:
        print(f"Caption: {post['caption']}")
        print(f"Image URL: {post['image_url']}")
    else:
        print("Failed to fetch post.")
