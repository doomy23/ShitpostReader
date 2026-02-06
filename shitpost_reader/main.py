"""
Main entry point for ShitpostReader.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

from .url_matcher import URLMatcher
from .scraper_runner import ScraperRunner
from .tts_service import TTSService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='ShitpostReader - Scrape websites and read content out loud'
    )
    parser.add_argument(
        'url',
        help='URL to scrape (e.g., https://boards.4chan.org/pol/thread/527886348)'
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
        tts = TTSService(rate=args.rate, volume=args.volume)
        tts.start()
    
    # Define callback to handle messages
    def message_handler(message: str):
        logger.info(f"Extracted: {message[:100]}...")
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
            logger.info("Waiting for TTS to finish...")
            # Give TTS time to finish speaking
            time.sleep(2)
            tts.stop()
    
    logger.info("ShitpostReader finished")


if __name__ == '__main__':
    main()
