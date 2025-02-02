"""Screenshot module for capturing web pages.

This module provides functionality for capturing screenshots of web pages
using Playwright as the backend.
"""

from .capture import take_screenshot, take_screenshot_sync

__all__ = ['take_screenshot', 'take_screenshot_sync']