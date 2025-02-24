

import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from wordpress_xmlrpc import Client

import torch
# print("PyTorch is working:", torch.__version__)

# def test_packages():
#
#     response = requests.get("https://www.example.com")
#     print("Requests is working:", response.status_code)
#
#     soup = BeautifulSoup("<html><body><h1>Test</h"
#                          "1></body></html>", "html.parser")
#     print("BeautifulSoup is working:", soup.h1.text)
#
#     summarizer=pipeline("summarization",model='facebook/bart-large-cnn')
#     summary=summarizer('This is a test sentence for summarization.',max_length=10,min_length=5,do_sample=False)
#     print("Transformers is working:", summary[0]['summary_text'])
#
#     try:
#         client=Client("https://yourblog.wordpress.com/xmlrpc.php", "username", "password")
#         print("WordPress XML-RPC is installed and ready.")
#     except Exception as e:
#         print("WordPress Error :",e)
#
# if __name__=="__main__":
#             test_packages()

# main.py
import logging
from scraper import NewsCrawler
from processor import ContentProcessor
from publisher import WordPressPublisher
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s',
    handlers=[logging.FileHandler('news_agent.log'), logging.StreamHandler()]
)


def main():
    """Autonomous AI Agent - Main Execution Flow"""
    try:
        load_dotenv()  # Load environment variables

        # Initialize components
        logging.info("Initializing components...")
        crawler = NewsCrawler()
        processor = ContentProcessor()
        publisher = WordPressPublisher()
        # Automated web crawling
        logging.info("Starting hierarchical web crawling...")
        articles = crawler.fetch_articles()
        logging.info(f"Processed {len(articles)} raw articles")

        # Content processing pipeline
        success_count = 0
        for article in articles:
            try:
                processed = processor.process_article(article)
                if not processed:
                    continue

                # Automated publishing
                post_id = publisher.publish(
                    title=article['title'],
                    content=processed['summary'],
                    seo_data=processed['seo_data'],

                )

                if post_id:
                    success_count += 1
                    logging.info(f"Published article ID: {post_id}")

                time.sleep(5)  # Rate limiting

            except Exception as e:
                logging.error(f"Failed to process article: {str(e)}")
                continue

        logging.info(f"Successfully published {success_count}/{len(articles)} articles")

    except Exception as e:
        logging.error(f"Critical failure: {str(e)}")
        raise


if __name__ == "__main__":
    main()



















