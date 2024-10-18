from playwright_stealth import stealth_async
from fake_useragent import UserAgent


async def stealth_page(page):
    """
    Apply stealth settings to a Playwright page, including using a random User-Agent.

    Parameters:
    - page (Page): The Playwright page to which stealth settings will be applied.

    Returns:
    Page: The modified Playwright page.

    Example:
    ```python
    async with async_playwright() as p:
        browser, page = await init_browser(p)
        page = await stealth_page(page)
        # Your code using the modified page goes here
    ```

    Note:
    - The 'playwright_stealth' module is used to apply additional stealth settings to the page.
    - The 'fake_useragent' library is used to generate a random User-Agent for increased anonymity.
    """
    # Use playwright_stealth for additional stealth settings
    await stealth_async(page)

    # # Webdriver
    # await page.add_init_script(
    #     """
    #     navigator.webdriver = false
    #     Object.defineProperty(navigator, 'webdriver', {
    #     get: () => false
    #     })
    #     """
    # )

    # Chrome
    await page.add_init_script(
        """
        window.chrome = {
            app: {},
            webstore: {},
            runtime: {},
            loadTimes: {},
        };
    """
    )

    # # Plugins
    # await page.add_init_script(
    #     """
    #     Object.defineProperty(navigator, 'plugins', {
    #         get: () => [
    #             { name: 'Plugin 1', description: 'Description of plugin 1', filename: 'plugin1.dll' },
    #             { name: 'Plugin 2', description: 'Description of plugin 2', filename: 'plugin2.dll' },
    #             { name: 'Plugin 3', description: 'Description of plugin 3', filename: 'plugin3.dll' },
    #             { name: 'Plugin 4', description: 'Description of plugin 4', filename: 'plugin4.dll' },
    #             { name: 'Plugin 5', description: 'Description of plugin 5', filename: 'plugin5.dll' },
    #         ],
    #     });
    # """
    # )

    # Permission
    await page.add_init_script(
        """
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => {
            if (parameters.name === 'notifications') {
                return Promise.resolve({ state: Notification.permission });
            } else {
                return originalQuery(parameters);
            }
        };
    """
    )

    # WebGL
    await page.add_init_script(
        """
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) {
                return 'Intel Inc.';  // Vendor
            }
            if (parameter === 37446) {
                return 'Intel Iris OpenGL Engine';  // Renderer
            }
            return getParameter(parameter);
        };
        """
    )

    # Canvas Fingerprint
    await page.add_init_script(
        """
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {
            if (type === 'image/png') {
                return "data:image/png;base64,fake_canvas_image_data";
            }
            return toDataURL.apply(this, arguments);
        };
        """
    )

    # Audio
    await page.add_init_script(
        """
        const getChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function() {
            const results = getChannelData.apply(this, arguments);
            for (let i = 0; i < results.length; i++) {
                results[i] = results[i] + Math.random() * 0.0000001;  // Add slight noise to spoof
            }
            return results;
        };
        """
    )

    # Web RTC
    await page.add_init_script(
        """
        Object.defineProperty(navigator, 'mediaDevices', {
            value: { getUserMedia: () => Promise.reject(new Error('WebRTC is disabled')) }
        });
        """
    )

    # Set a random User-Agent using fake_useragent
    ua = UserAgent(browsers=["chrome"])
    user_agent = ua.random
    await page.set_extra_http_headers({"User-Agent": user_agent})

    return page


async def init_browser(
    playwright, headless: bool = True, browser: str = "chromium", proxy: str = None
):
    """
    Initialize a browser and create a new page with optional stealth settings.

    Parameters:
    - playwright (Playwright): An instance of the Playwright class.
    - headless (bool, optional): Whether to run the browser in headless mode. Default is True.
    - browser (str, optional): The browser to launch. Valid options are "chromium" (default), "firefox", or "webkit".
    - proxy (str, optional): Proxy server to use in the format "protocol://username:password@host:port". Default is None.

    Returns:
    tuple: A tuple containing the browser instance and the newly created page.

    Example:
    ```python
    async with async_playwright() as p:
        browser, page = await init_browser(p, headless=False, browser="firefox", proxy="http://username:password@proxy-server:8080")
        # Your code using the browser and page goes here
        await browser.close()
    ```

    Note:
    - If using a proxy, make sure to provide it in the format "protocol://username:password@host:port".
    - The 'stealth' module is used to apply stealth settings to the page, enhancing the browser automation stealthiness.
    """

    if browser == "firefox":
        chromium = playwright.firefox
    elif browser == "webkit":
        chromium = playwright.webkit
    else:
        chromium = playwright.chromium

    if proxy:
        browser = await chromium.launch(
            headless=headless,
            proxy=proxy,
        )
    else:
        browser = await chromium.launch(headless=headless)

    page = await browser.new_page()
    page = await stealth_page(page)

    return browser, page
