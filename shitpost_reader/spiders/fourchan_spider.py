"""
4chan spider for scraping thread messages.
"""

import json
import re
from .base_spider import BaseSpider
from shitpost_reader.url_matcher import URLMatcher
from shitpost_reader.logger import logger


class FourChanSpider(BaseSpider):
    """Spider for scraping 4chan threads."""
    
    name = "4chan"
    
    def parse(self, response):
        """
        Parse a 4chan thread page.
        
        Args:
            response: The HTTP response from the thread page.
        """
        # Extract the original post (OP)
        op_post = response.css('div.opContainer')
        if op_post:
            # Get the post content
            op_message = op_post.css('blockquote.postMessage::text').getall()
            if op_message:
                op_text = ' '.join(op_message).strip()
                if op_text:
                    self.handle_message(f"{op_text}")
        
        # Extract all replies
        reply_posts = response.css('div.replyContainer')
        for post in reply_posts:
            # Get the message content
            message_parts = post.css('blockquote.postMessage::text').getall()
            if message_parts:
                message_text = ' '.join(message_parts).strip()
                if message_text:
                    self.handle_message(f"{message_text}")
        
        logger.info(f"Finished parsing thread: {response.url}")


class FourChanCatalogSpider(FourChanSpider):
    """Spider for scraping 4chan catalog pages."""
    
    name = "4chan_catalog"
    url_matcher = URLMatcher()
    
    def parse(self, response):
        """
        Parse a 4chan catalog page to extract thread links and scrape them.
        
        Args:
            response: The HTTP response from the catalog page.
        """
        # Get the board name from the URL
        board_match = re.search(r'boards\.4chan\.org/([^/]+)/catalog', response.url)
        if not board_match:
            logger.error(f"Could not determine board from URL: {response.url}")
            return
        board = board_match.group(1)

        # Extract all thread links from the catalog
        pattern = r'var catalog = ({.*?});'
        match = re.search(pattern, response.text, re.DOTALL)
        if match:
            # Parse JSON
            catalog_json = match.group(1)
            catalog = json.loads(catalog_json)
            
            # Extract thread IDs (keys of the "threads" object)
            thread_ids = set(catalog['threads'].keys())

            # Process each thread link
            for count, id in enumerate(thread_ids):
                if id is not None and count < self.threads:
                    # Construct full URL if necessary
                    link = f"https://boards.4chan.org/{board}/thread/{id}"
                    logger.info(f"Processing thread link: {link}")
                    yield response.follow(link, callback=self.parse_thread)
                else:
                    logger.info(f"Skipping thread with ID: {id}")
        
        logger.info(f"Finished parsing catalog: {response.url}")
    
    def parse_thread(self, response):
        """Parse an individual thread page."""
        # Extract thread ID from URL        
        id_match = re.search(r'thread/(\d+)', response.url)
        id = id_match.group(1) if id_match else "unknown"
        self.handle_message(f"Thread {id}")
        super().parse(response)
