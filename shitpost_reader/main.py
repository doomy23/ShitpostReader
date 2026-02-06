"""
Main entry point for ShitpostReader.
"""

import argparse
from email.mime import message
import logging
import sys
import time
from pathlib import Path

from .url_matcher import URLMatcher
from .scraper_runner import ScraperRunner
from .tts_service import TTSService

# Set up logging
from .logger import logger


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='ShitpostReader - Scrape websites and read content out loud'
    )
    parser.add_argument(
        'url',
        help='URL to scrape (e.g., https://boards.4chan.org/pol/thread/000000000)'
    )
    parser.add_argument(
        '--rate',
        type=int,
        default=150,
        help='Speech rate in words per minute (default: 150)'
    )
    parser.add_argument(
        '--volume',
        type=float,
        default=0.9,
        help='Volume level from 0.0 to 1.0 (default: 0.9)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to custom scrapers.json configuration file'
    )
    parser.add_argument(
        '--no-tts',
        action='store_true',
        help='Disable text-to-speech output (just print messages)'
    )
    parser.add_argument(
        '--save',
        help='Saves the spoken output to an mp3 file'
    )
    
    args = parser.parse_args()
    
    # Initialize components
    logger.info("Starting ShitpostReader")
    logger.info(f"Target URL: {args.url}")
    
    # Match URL to scraper
    matcher = URLMatcher(config_path=args.config)
    match = matcher.match(args.url)
    
    if not match:
        logger.error(f"No scraper found for URL: {args.url}")
        logger.error("Supported patterns:")
        for scraper in matcher.scrapers:
            logger.error(f"  - {scraper['name']}: {scraper['description']}")
        sys.exit(1)
    
    logger.info(f"Using scraper: {match['name']} ({match['scraper_class']})")
    
    # Initialize TTS service
    tts = None
    if not args.no_tts:
        tts = TTSService(rate=args.rate, volume=args.volume, save_to_file=args.save)
        tts.start()

    def remove_urls(text: str) -> str:
        """Remove URLs from the given text."""
        import re
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)
    
    # Define callback to handle messages
    def message_handler(message: str):
        message = remove_urls(message.replace('\n', ' '))
        if tts:
            tts.speak(message)
        else:
            print(message)
    
    # Run the scraper
    try:
        runner = ScraperRunner()
        runner.run(
            url=args.url,
            scraper_class=match['scraper_class'],
            callback=message_handler
        )
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error during scraping: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if tts:
            tts.wait_until_done()
    
    logger.info("ShitpostReader finished")


if __name__ == '__main__':
    main()
