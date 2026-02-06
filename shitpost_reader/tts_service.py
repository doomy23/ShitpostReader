"""
Text-to-speech service using pyttsx3.
"""

import time
import pyttsx3
from queue import Queue, Empty

# Set up logging
from .logger import logger


class TTSService:
    """Text-to-speech service that runs in background."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9, save_to_file: str = None):
        """
        Initialize the TTS service.
        
        Args:
            rate: Speech rate (words per minute).
            volume: Volume level (0.0 to 1.0).
        """
        self.rate = rate
        self.volume = volume
        self.queue = Queue()
        self.running = False
        self.is_speaking = False
        self.engine = None
        self.save_to_file = save_to_file
        
    def start(self):
        """Start the TTS service in background."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            self.running = True
            logger.info("TTS service started")
        except (RuntimeError, ImportError) as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            logger.error("TTS will not be available. Install espeak/espeak-ng on Linux or use --no-tts flag.")
    
    def stop(self):
        """Stop the TTS service."""
        self.running = False
        logger.info("TTS service stopped")
    
    def speak(self, text: str):
        """
        Add text to the speech queue.
        
        Args:
            text: The text to speak.
        """
        self.queue.put(text)
    
    def wait_until_done(self):
        """
        Wait until all queued speech is finished.
        
        Returns:
            True if finished, False if timeout occurred.
        """
        self._process_queue()
        return True
    
    def _process_queue(self):
        """Process the speech queue in the background."""
        
        fulltext = ""
        self.is_speaking = True
        while not self.queue.empty():
            text = self.queue.get()
            logger.info(f"TTS speaking: {text[:100]}...")
            self.engine.say(text)
            fulltext += text + " "

        self.engine.startLoop(False)
        while self.engine.isBusy():
            time.sleep(0.1)
            self.engine.iterate()
        self.engine.endLoop()
        self.is_speaking = False

        if self.save_to_file:
            self.engine.save_to_file(fulltext, f"output/{self.save_to_file}")
            self.engine.runAndWait()
        
        try:
            self.engine.stop()
        except Exception:
            pass  # Engine may already be stopped
        self.stop()
