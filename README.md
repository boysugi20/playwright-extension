
# Playwright Extension

A simple Python package designed to enhance your web automation experience with [Playwright](https://playwright.dev/python/). 
This extension integrates seamlessly with Playwright to provide additional functionality, including the incorporation of [playwright_stealth](https://github.com/AtuboDad/playwright_stealth) for improved bot detection evasion and robust proxy support for secure and anonymous browsing.

Key Features:
- Enhanced Bot Detection Evasion: Leveraging playwright_stealth, this package helps mimic real user behavior, reducing the risk of detection by sophisticated anti-bot systems.
- Proxy Support: Easily configure and manage proxies to ensure privacy and anonymity during your web scraping or automation tasks.
- Extensible Functions: Add custom functions tailored to your specific automation needs, enhancing the overall functionality of Playwright.

## Installation

You can install this package using:

```bash
pip install git+https://github.com/boysugi20/playwright-extension.git
```

## Usage
```python
from playwright_extension import module
from playwright.async_api import async_playwright
import asyncio

PROXY = {"server": "http://myproxy.com:3128", "username": "usr", "password": "pwd"}

async def main():

    async with async_playwright() as playwright:

        browser, page = await module.init_browser(
            playwright, headless=False, browser="chromium", proxy=PROXY
        )

        await page.goto("http://bot.sannysoft.com")
        await page.screenshot(path="example.png", full_page=True)

        await browser.close()

asyncio.run(main())
```

## Result
http://bot.sannysoft.com
![result-example](https://github.com/user-attachments/assets/3df09da0-43b7-4469-9921-5c0db6e8694d)
