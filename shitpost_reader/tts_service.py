"""
Text-to-speech service using pyttsx3.
"""

import pyttsx3
from threading import Thread
from queue import Queue, Empty
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
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
        except (RuntimeError, ImportError) as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            logger.error("TTS will not be available. Install espeak/espeak-ng on Linux or use --no-tts flag.")
            return
        
        while self.running:
            try:
                text = self.queue.get(timeout=1)
                if text is None:  # Stop signal
                    break
                
                logger.info(f"Speaking: {text[:50]}...")
                engine.say(text)
                engine.runAndWait()
                
            except Empty:
                # Timeout waiting for queue item, continue loop
                continue
            except RuntimeError as e:
                logger.error(f"TTS engine error: {e}")
                if not self.running:
                    break
            except Exception as e:
                logger.error(f"Unexpected error in TTS service: {e}")
                if not self.running:
                    break
        
        try:
            engine.stop()
        except Exception:
            pass  # Engine may already be stopped
        logger.info("TTS service thread ended")
