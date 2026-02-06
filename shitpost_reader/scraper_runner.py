"""
Scraper runner to execute spiders with Scrapy.
"""

from scrapy.crawler import CrawlerProcess
from typing import Callable

from .spiders.fourchan_spider import FourChanSpider, FourChanCatalogSpider

# Set up logging
from .logger import logger


# Map of scraper class names to actual classes
SPIDER_REGISTRY = {
    'FourChanSpider': FourChanSpider,
    'FourChanCatalogSpider': FourChanCatalogSpider,
}


class ScraperRunner:
    """Runner for executing spiders."""
    
    def __init__(self):
        """Initialize the scraper runner."""
        self.process = None
    
    def run(self, url: str, scraper_class: str, callback: Callable, threads: int = 10):
        """
        Run a scraper for the given URL.
        
        Args:
            url: The URL to scrape.
            scraper_class: The name of the spider class to use.
            callback: Callback function to handle extracted messages.
            threads: Maximum number of threads to use for scraping.
        """
        spider_class = SPIDER_REGISTRY.get(scraper_class)
        if not spider_class:
            raise ValueError(f"Unknown scraper class: {scraper_class}")
        
        # Configure Scrapy settings
        settings = {
            'LOG_LEVEL': 'INFO',
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'ROBOTSTXT_OBEY': False,  # 4chan doesn't have a robots.txt for threads
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 1,
        }
        
        # Create and configure the crawler process
        self.process = CrawlerProcess(settings)
        
        # Add the spider to the process
        self.process.crawl(spider_class, url=url, callback=callback, threads=threads)
        
        # Run the crawler
        logger.info(f"Starting scraper for URL: {url}")
        self.process.start()
        logger.info("Scraping completed")
