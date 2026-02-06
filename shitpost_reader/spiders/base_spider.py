"""
Base spider class for ShitpostReader.
"""

import scrapy
from typing import Optional, Callable

# Set up logging
from shitpost_reader.logger import logger


class BaseSpider(scrapy.Spider):
    """Base spider class for all ShitpostReader spiders."""
    
    name = "base"
    threads = None
    posts = None
    count = 0
    
    def __init__(self, url: str, callback: Optional[Callable] = None, threads: int = 10, posts: int = float('inf'), *args, **kwargs):
        """
        Initialize the spider.
        
        Args:
            url: The URL to scrape.
            callback: Optional callback function to handle extracted messages.
            threads: Maximum number of threads to use for scraping.
            posts: Maximum number of posts to read.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.message_callback = callback
        self.threads = threads
        self.posts = posts
    
    def parse(self, response):
        """Parse the response. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the parse method")
    
    def handle_message(self, message: str):
        """
        Handle an extracted message.
        
        Args:
            message: The extracted message text.
        """
        if self.count >= self.posts:
            self.crawler.engine.close_spider(self, reason='post_limit_reached')
            return
        if self.message_callback:
            self.message_callback(message)
        else:
            logger.info(f"Message: {message}")
        self.count += 1
