"""
URL matcher module to identify which scraper to use based on URL patterns.
"""

import json
import re
from pathlib import Path
from typing import Optional, Dict, Any


class URLMatcher:
    """Matches URLs against scraper patterns defined in scrapers.json."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the URL matcher.
        
        Args:
            config_path: Path to the scrapers.json configuration file.
                        If None, uses the default scrapers.json in the package root.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "scrapers.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Compile regex patterns for efficiency
        self.scrapers = []
        for scraper in self.config.get('scrapers', []):
            pattern = scraper.get('url_pattern')
            if pattern:
                self.scrapers.append({
                    'name': scraper.get('name'),
                    'pattern': re.compile(pattern),
                    'scraper_class': scraper.get('scraper_class'),
                    'description': scraper.get('description')
                })
    
    def match(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Match a URL against known scraper patterns.
        
        Args:
            url: The URL to match.
        
        Returns:
            Dictionary with scraper information if matched, None otherwise.
        """
        for scraper in self.scrapers:
            if scraper['pattern'].match(url):
                return {
                    'name': scraper['name'],
                    'scraper_class': scraper['scraper_class'],
                    'description': scraper['description']
                }
        return None
