# Quick Start Guide

## Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/doomy23/ShitpostReader.git
cd ShitpostReader

# 2. Install system dependencies (Linux only)
# Ubuntu/Debian:
sudo apt-get install espeak espeak-ng

# Fedora:
# sudo dnf install espeak espeak-ng

# 3. Install Python dependencies
pip install -r requirements.txt
```

## Basic Usage

### Scrape and Read a 4chan Thread

```bash
# With text-to-speech (will read out loud)
python -m shitpost_reader.main "https://boards.4chan.org/pol/thread/527886348"

# Without audio (just print to console)
python -m shitpost_reader.main "https://boards.4chan.org/pol/thread/527886348" --no-tts
```

### Customize Speech Settings

```bash
# Speak faster (default is 150 WPM)
python -m shitpost_reader.main "URL" --rate 200

# Adjust volume (0.0 to 1.0, default is 0.9)
python -m shitpost_reader.main "URL" --volume 0.7

# Combine options
python -m shitpost_reader.main "URL" --rate 180 --volume 0.8
```

## Example Output

```
2026-02-06 10:00:00,000 - __main__ - INFO - Starting ShitpostReader
2026-02-06 10:00:00,001 - __main__ - INFO - Target URL: https://boards.4chan.org/pol/thread/527886348
2026-02-06 10:00:00,002 - __main__ - INFO - Using scraper: 4chan (FourChanSpider)
2026-02-06 10:00:00,100 - __main__ - INFO - Extracted: Original Post: Welcome to the thread...
2026-02-06 10:00:00,150 - __main__ - INFO - Extracted: Reply 123456789: First reply here...
2026-02-06 10:00:00,200 - __main__ - INFO - Extracted: Reply 123456790: Another reply...
...
```

## Supported Websites

Currently supported:
- **4chan threads**: `https://boards.4chan.org/[board]/thread/[id]`

Want to add more sites? See [CONTRIBUTING.md](CONTRIBUTING.md)

## Troubleshooting

### TTS not working?

**Linux:** Install espeak
```bash
sudo apt-get install espeak espeak-ng
```

**macOS/Windows:** Should work out of the box with native engines

### "No scraper found for URL" error?

Make sure your URL matches one of the supported patterns:
```bash
# Check supported patterns
python -m shitpost_reader.main "https://invalid-url.com"
```

### Import errors?

Make sure dependencies are installed:
```bash
pip install -r requirements.txt
```

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔧 Learn how to add new scrapers in [CONTRIBUTING.md](CONTRIBUTING.md)
- 💡 Check out [examples/basic_usage.py](examples/basic_usage.py) for code examples

## Need Help?

- Check existing issues on GitHub
- Review the [CONTRIBUTING.md](CONTRIBUTING.md) guide
- Look at example implementations in `shitpost_reader/spiders/`
