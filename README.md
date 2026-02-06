# ShitpostReader

A Python 3.11+ project that scrapes specific texts from websites and reads them out loud using text-to-speech.

## Features

- 🕷️ Uses Scrapy to scrape content from supported websites
- 🔊 Reads content out loud using pyttsx3
- 🧵 Supports scraping 4chan threads
- 🎯 Extensible architecture with JSON-based scraper configuration
- 🔄 Background TTS processing

## Installation

```bash
# Clone the repository
git clone https://github.com/doomy23/ShitpostReader.git
cd ShitpostReader

# Install dependencies
pip install -r requirements.txt

# Or install the package
pip install -e .
```

## Usage

### Basic Usage

```bash
# Scrape and read a 4chan thread
python -m shitpost_reader.main "https://boards.4chan.org/pol/thread/527886348"

# Or use the installed command
shitpost-reader "https://boards.4chan.org/pol/thread/527886348"
```

### Command Line Options

```bash
# Adjust speech rate (words per minute)
python -m shitpost_reader.main "URL" --rate 200

# Adjust volume (0.0 to 1.0)
python -m shitpost_reader.main "URL" --volume 0.7

# Print messages without TTS
python -m shitpost_reader.main "URL" --no-tts

# Use custom scraper configuration
python -m shitpost_reader.main "URL" --config path/to/scrapers.json
```

## Supported Sites

Currently supported:
- **4chan**: Thread URLs like `https://boards.4chan.org/[board]/thread/[id]`

## Architecture

### Components

1. **URL Matcher** (`url_matcher.py`): Matches URLs against regex patterns defined in `scrapers.json` to determine which scraper to use.

2. **Scrapers Configuration** (`scrapers.json`): JSON file defining URL patterns and their corresponding spider classes.

3. **Spiders** (`spiders/`): Scrapy spiders for extracting content from specific websites.
   - `base_spider.py`: Base spider class
   - `fourchan_spider.py`: Spider for 4chan threads

4. **TTS Service** (`tts_service.py`): Background text-to-speech service using pyttsx3.

5. **Scraper Runner** (`scraper_runner.py`): Manages Scrapy crawler execution.

6. **Main** (`main.py`): Command-line interface and application entry point.

## Adding New Scrapers

1. Add a new spider class in `shitpost_reader/spiders/`:

```python
from .base_spider import BaseSpider

class MySpider(BaseSpider):
    name = "mysite"
    
    def parse(self, response):
        # Extract content and call self.handle_message(text)
        pass
```

2. Register the spider in `scraper_runner.py`:

```python
SPIDER_REGISTRY = {
    'MySpider': MySpider,
}
```

3. Add configuration to `scrapers.json`:

```json
{
  "name": "mysite",
  "url_pattern": "^https?://mysite\\.com/.*",
  "scraper_class": "MySpider",
  "description": "Scraper for mysite.com"
}
```

## Requirements

- Python 3.11+
- Scrapy >= 2.11.0
- pyttsx3 >= 2.90
- requests >= 2.31.0

## License

See LICENSE file for details.
