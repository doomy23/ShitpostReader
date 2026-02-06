#!/usr/bin/env python3
"""
Example: Basic usage of ShitpostReader to scrape and read a 4chan thread.

This example demonstrates:
1. How to use the URL matcher
2. How to run the scraper with TTS disabled (for testing)
3. How to customize speech settings
"""

import sys
from pathlib import Path

# Add the package to the path if running from examples directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from shitpost_reader.url_matcher import URLMatcher
from shitpost_reader.scraper_runner import ScraperRunner
from shitpost_reader.tts_service import TTSService


def example_basic_usage():
    """Basic example: scrape without TTS."""
    print("Example 1: Basic Scraping (No TTS)")
    print("=" * 70)
    
    # The URL to scrape
    url = "https://boards.4chan.org/pol/thread/527886348"
    
    # Match the URL to a scraper
    matcher = URLMatcher()
    match = matcher.match(url)
    
    if not match:
        print(f"Error: No scraper found for URL: {url}")
        return
    
    print(f"Using scraper: {match['name']}")
    print(f"Spider class: {match['scraper_class']}")
    
    # Define a callback to handle extracted messages
    def message_handler(message):
        print(f"[MESSAGE] {message[:80]}...")
    
    # Run the scraper
    runner = ScraperRunner()
    try:
        runner.run(
            url=url,
            scraper_class=match['scraper_class'],
            callback=message_handler
        )
    except Exception as e:
        print(f"Error during scraping: {e}")


def example_with_tts():
    """Example with TTS enabled."""
    print("\nExample 2: Scraping with Text-to-Speech")
    print("=" * 70)
    
    url = "https://boards.4chan.org/pol/thread/527886348"
    
    # Initialize TTS service
    tts = TTSService(rate=175, volume=0.8)
    tts.start()
    
    # Match the URL
    matcher = URLMatcher()
    match = matcher.match(url)
    
    if not match:
        print(f"Error: No scraper found for URL: {url}")
        return
    
    # Define callback to both print and speak
    def message_handler(message):
        print(f"[SPEAKING] {message[:80]}...")
        tts.speak(message)
    
    # Run the scraper
    runner = ScraperRunner()
    try:
        runner.run(
            url=url,
            scraper_class=match['scraper_class'],
            callback=message_handler
        )
        
        # Wait for TTS to finish
        import time
        print("\nWaiting for TTS to complete...")
        time.sleep(2)
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        tts.stop()


def example_custom_scraper_config():
    """Example using a custom scraper configuration."""
    print("\nExample 3: Using Custom Scraper Configuration")
    print("=" * 70)
    
    # You can create your own scrapers.json with custom patterns
    # For this example, we'll just use the default
    
    url = "https://boards.4chan.org/g/thread/123456789"
    
    # Load custom config (None = use default)
    matcher = URLMatcher(config_path=None)
    match = matcher.match(url)
    
    if match:
        print(f"✓ URL matched to: {match['name']}")
        print(f"  Scraper class: {match['scraper_class']}")
        print(f"  Description: {match['description']}")
    else:
        print("✗ URL did not match any scraper")


if __name__ == '__main__':
    print("ShitpostReader Examples")
    print("=" * 70)
    print()
    
    # Run example 1 (basic scraping)
    # example_basic_usage()
    
    # Run example 2 (with TTS) - commented out as it requires audio
    # example_with_tts()
    
    # Run example 3 (custom config)
    example_custom_scraper_config()
    
    print("\n" + "=" * 70)
    print("To run the actual scraper from command line:")
    print("  python -m shitpost_reader.main <URL>")
    print("  python -m shitpost_reader.main <URL> --no-tts")
    print("  python -m shitpost_reader.main <URL> --rate 200 --volume 0.8")
