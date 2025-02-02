#!/usr/bin/env python3

import asyncio
import logging
from pathlib import Path
import tempfile
from typing import Optional, Dict, Any

from playwright.async_api import async_playwright, Page

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

async def take_screenshot(
    url: str,
    output_path: Optional[str] = None,
    width: int = 1280,
    height: int = 720,
    full_page: bool = True,
    wait_until: str = 'networkidle',
    viewport_options: Optional[Dict[str, Any]] = None
) -> str:
    """Take a screenshot of a webpage using Playwright.

    Args:
        url: The URL to take a screenshot of.
        output_path: Path to save the screenshot. If None, saves to a temporary file.
        width: Viewport width. Defaults to 1280.
        height: Viewport height. Defaults to 720.
        full_page: Whether to take a screenshot of the full scrollable page. Defaults to True.
        wait_until: When to consider navigation succeeded. Defaults to 'networkidle'.
        viewport_options: Additional viewport options to pass to Playwright.

    Returns:
        str: Path to the saved screenshot.

    Raises:
        PlaywrightError: If there's an error during screenshot capture.
        ValueError: If the URL or output path is invalid.
    """
    logger.debug(f"Starting screenshot capture for URL: {url}")
    logger.debug(f"Screenshot parameters - full_page: {full_page}, wait_until: {wait_until}")
    
    if not url.startswith(('http://', 'https://')): 
        logger.error(f"Invalid URL format: {url}")
        raise ValueError(f"Invalid URL: {url}. Must start with http:// or https://")

    if output_path is None:
        temp_dir = Path('/tmp')
        temp_file = tempfile.NamedTemporaryFile(dir=str(temp_dir), suffix='.png', delete=False)
        output_path = temp_file.name
        temp_file.close()
        logger.debug(f"Created temporary file for screenshot in /tmp: {output_path}")
    else:
        output_dir = Path(output_path).parent
        logger.debug(f"Ensuring output directory exists: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

    viewport = viewport_options or {'width': width, 'height': height}
    logger.debug(f"Using viewport settings: {viewport}")

    try:
        logger.debug("Initializing Playwright")
        async with async_playwright() as p:
            logger.debug("Launching browser in headless mode")
            browser = await p.chromium.launch(headless=True)
            logger.debug("Creating new browser page with viewport settings")
            page = await browser.new_page(viewport=viewport)

            try:
                logger.info(f"Navigating to URL: {url}")
                await page.goto(url, wait_until=wait_until)
                logger.debug(f"Page loaded successfully, waiting condition: {wait_until}")
                
                logger.info(f"Capturing screenshot to: {output_path}")
                await page.screenshot(path=output_path, full_page=full_page)
                logger.info(f"Screenshot saved successfully to {output_path}")
                return output_path
            finally:
                logger.debug("Closing browser")
                await browser.close()
    except Exception as e:
        logger.error(f"Error during screenshot capture: {str(e)}", exc_info=True)
        raise

def take_screenshot_sync(
    url: str,
    output_path: Optional[str] = None,
    width: int = 1280,
    height: int = 720,
    full_page: bool = True,
    wait_until: str = 'networkidle',
    viewport_options: Optional[Dict[str, Any]] = None
) -> str:
    """Synchronous wrapper for take_screenshot.

    This function provides a synchronous interface to the asynchronous take_screenshot function.
    All parameters are passed directly to take_screenshot.

    Returns:
        str: Path to the saved screenshot.
    """
    logger.debug("Starting synchronous screenshot capture")
    result = asyncio.run(take_screenshot(
        url=url,
        output_path=output_path,
        width=width,
        height=height,
        full_page=full_page,
        wait_until=wait_until,
        viewport_options=viewport_options
    ))
    logger.debug("Synchronous screenshot capture completed")
    return result