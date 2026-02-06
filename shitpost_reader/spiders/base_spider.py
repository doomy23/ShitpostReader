"""
Base spider class for ShitpostReader.
"""

import scrapy
from typing import Optional, Callable


class BaseSpider(scrapy.Spider):
    """Base spider class for all ShitpostReader spiders."""
    
    name = "base"
    
    def __init__(self, url: str, callback: Optional[Callable] = None, *args, **kwargs):
        """
        Initialize the spider.
        
        Args:
            url: The URL to scrape.
            callback: Optional callback function to handle extracted messages.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.message_callback = callback
    
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
            self.logger.info(f"Message: {message}")
