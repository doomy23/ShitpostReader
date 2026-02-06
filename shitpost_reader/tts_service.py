"""
Text-to-speech service using pyttsx3.
"""

import pyttsx3
from threading import Thread
from queue import Queue
import logging

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-speech service that runs in a background thread."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
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
        self.thread = None
        
    def start(self):
        """Start the TTS service in a background thread."""
        if self.running:
            logger.warning("TTS service is already running")
            return
        
        self.running = True
        self.thread = Thread(target=self._process_queue, daemon=True)
        self.thread.start()
        logger.info("TTS service started")
    
    def stop(self):
        """Stop the TTS service."""
        self.running = False
        self.queue.put(None)  # Signal to stop
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("TTS service stopped")
    
    def speak(self, text: str):
        """
        Add text to the speech queue.
        
        Args:
            text: The text to speak.
        """
        if not self.running:
            logger.warning("TTS service is not running, starting it now")
            self.start()
        
        self.queue.put(text)
    
    def _process_queue(self):
        """Process the speech queue in the background."""
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        
        while self.running:
            try:
                text = self.queue.get(timeout=1)
                if text is None:  # Stop signal
                    break
                
                logger.info(f"Speaking: {text[:50]}...")
                engine.say(text)
                engine.runAndWait()
                
            except Exception as e:
                if self.running:  # Only log if not shutting down
                    logger.error(f"Error in TTS service: {e}")
        
        engine.stop()
        logger.info("TTS service thread ended")
