"""
4chan spider for scraping thread messages.
"""

import scrapy
from .base_spider import BaseSpider


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
            # Get post number
            post_num = post.css('span.postNum a::text').get()
            
            # Get the message content
            message_parts = post.css('blockquote.postMessage::text').getall()
            if message_parts:
                message_text = ' '.join(message_parts).strip()
                if message_text:
                    self.handle_message(f"{message_text}")
        
        self.logger.info(f"Finished parsing thread: {response.url}")
