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
    
    def __init__(self, url: str, callback: Optional[Callable] = None, threads: int = 100, *args, **kwargs):
        """
        Initialize the spider.
        
        Args:
            url: The URL to scrape.
            callback: Optional callback function to handle extracted messages.
            threads: Maximum number of threads to use for scraping.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.message_callback = callback
        self.threads = threads
    
    def parse(self, response):
        """Parse the response. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the parse method")
    
    def handle_message(self, message: str):
        """
        Handle an extracted message.
        
        Args:
            message: The extracted message text.
        """
        if self.message_callback:
            self.message_callback(message)
        else:
            logger.info(f"Message: {message}")
