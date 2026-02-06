# Adding New Scrapers to ShitpostReader

This guide explains how to add support for new websites to ShitpostReader.

## Overview

To add a new scraper, you need to:
1. Create a new spider class
2. Register the spider in the runner
3. Add the URL pattern to the configuration

## Step-by-Step Guide

### 1. Create a New Spider Class

Create a new file in `shitpost_reader/spiders/` for your spider:

```python
# shitpost_reader/spiders/reddit_spider.py
from .base_spider import BaseSpider


class RedditSpider(BaseSpider):
    """Spider for scraping Reddit posts and comments."""
    
    name = "reddit"
    
    def parse(self, response):
        """
        Parse a Reddit page.
        
        Args:
            response: The HTTP response from the page.
        """
        # Extract the main post
        post_title = response.css('h1::text').get()
        post_content = response.css('div.post-content::text').get()
        
        if post_title:
            self.handle_message(f"Post: {post_title}")
        
        if post_content:
            self.handle_message(post_content)
        
        # Extract comments
        comments = response.css('div.comment')
        for comment in comments:
            text = comment.css('div.comment-text::text').get()
            if text:
                self.handle_message(f"Comment: {text}")
```

### 2. Register the Spider

Add your spider to the `SPIDER_REGISTRY` in `shitpost_reader/scraper_runner.py`:

```python
from .spiders.fourchan_spider import FourChanSpider
from .spiders.reddit_spider import RedditSpider  # Add this import

SPIDER_REGISTRY = {
    'FourChanSpider': FourChanSpider,
    'RedditSpider': RedditSpider,  # Add this line
}
```

### 3. Add Configuration

Add your scraper configuration to `scrapers.json`:

```json
{
  "scrapers": [
    {
      "name": "4chan",
      "url_pattern": "^https?://boards\\.4chan\\.org/[^/]+/thread/\\d+",
      "scraper_class": "FourChanSpider",
      "description": "Scraper for 4chan threads"
    },
    {
      "name": "reddit",
      "url_pattern": "^https?://(?:www\\.)?reddit\\.com/r/[^/]+/comments/[^/]+",
      "scraper_class": "RedditSpider",
      "description": "Scraper for Reddit posts"
    }
  ]
}
```

## Spider Development Tips

### Using Scrapy Selectors

Scrapy provides powerful CSS and XPath selectors:

```python
# CSS selectors
response.css('div.content::text').get()      # Get first match
response.css('div.content::text').getall()   # Get all matches
response.css('a::attr(href)').get()          # Get attribute

# XPath selectors
response.xpath('//div[@class="content"]/text()').get()
```

### Handling Messages

Always use `self.handle_message()` to process extracted text:

```python
def parse(self, response):
    text = response.css('div.content::text').get()
    if text:
        self.handle_message(text)
```

### Testing Your Spider

Create a test script with mock HTML:

```python
from scrapy.http import HtmlResponse, Request
from shitpost_reader.spiders.myspider import MySpider

mock_html = """<html>...</html>"""
test_url = "https://example.com/page"

def callback(message):
    print(f"Extracted: {message}")

spider = MySpider(url=test_url, callback=callback)
request = Request(url=test_url)
response = HtmlResponse(
    url=test_url,
    request=request,
    body=mock_html.encode('utf-8'),
    encoding='utf-8'
)

spider.parse(response)
```

### Error Handling

Handle missing elements gracefully:

```python
def parse(self, response):
    # Use .get() which returns None if element not found
    title = response.css('h1::text').get()
    if title:
        self.handle_message(f"Title: {title}")
    
    # Use .getall() for multiple elements
    comments = response.css('div.comment::text').getall()
    for comment in comments:
        if comment.strip():  # Skip empty comments
            self.handle_message(comment)
```

## Common Patterns

### Pagination

If you need to follow links to other pages:

```python
def parse(self, response):
    # Extract content from current page
    for item in response.css('div.item'):
        text = item.css('::text').get()
        self.handle_message(text)
    
    # Follow pagination links
    next_page = response.css('a.next::attr(href)').get()
    if next_page:
        yield response.follow(next_page, self.parse)
```

### JSON APIs

If the site uses JSON APIs:

```python
import json

def parse(self, response):
    data = json.loads(response.text)
    
    for item in data.get('items', []):
        text = item.get('text', '')
        if text:
            self.handle_message(text)
```

### User-Agent and Headers

Configure in the spider if needed:

```python
class MySpider(BaseSpider):
    name = "mysite"
    custom_settings = {
        'USER_AGENT': 'MyBot/1.0',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/json',
        }
    }
```

## Regex Pattern Tips

Common regex patterns for `url_pattern`:

```regex
# Match specific domain with any path
^https?://example\\.com/.*

# Match domain with specific path structure
^https?://example\\.com/category/[^/]+/item/\\d+

# Match subdomain
^https?://sub\\.example\\.com/.*

# Match HTTP or HTTPS
^https?://

# Match optional www
^https?://(?:www\\.)?example\\.com/

# Match any of multiple TLDs
^https?://example\\.(com|org|net)/
```

## Testing Checklist

Before submitting your scraper:

- [ ] Spider extracts all relevant text
- [ ] Empty/missing elements are handled gracefully
- [ ] URL pattern matches all expected URLs
- [ ] URL pattern doesn't match unintended URLs
- [ ] Spider is registered in `SPIDER_REGISTRY`
- [ ] Configuration is added to `scrapers.json`
- [ ] Code follows the existing style
- [ ] Tested with mock HTML
- [ ] Respects website's robots.txt (if applicable)

## Example: Complete Implementation

See `examples/basic_usage.py` for a complete example of using the scraper system.

For reference implementation, see `shitpost_reader/spiders/fourchan_spider.py`.
