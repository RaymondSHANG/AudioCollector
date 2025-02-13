from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

def get_correct_url(url: str) -> str:
    """
    Convert Google News URL to its original source URL using Playwright.

    Args:
        url (str): The input URL to process

    Returns:
        str: The resolved URL pointing to the original news source

    Raises:
        ValueError: If URL resolution fails or hits Google's rate limit
        Exception: If browser automation fails
        TimeoutError: If URL resolution timed out after 60 seconds
    """
    if not url.startswith("https://news.google.com"):
        return url

    with sync_playwright() as p:
        # Launch browser with specific configurations
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        try:
            context = browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()

            # Navigate to URL and wait for redirect
            page.goto(url, wait_until="networkidle")
            try:
                page.wait_for_url(
                    lambda url: not url.startswith("https://news.google.com"),
                    timeout=60000,
                )
            except PlaywrightTimeoutError:
                raise ValueError("URL resolution timed out after 60 seconds")

            final_url = page.url
            if "google.com/sorry" in final_url:
                raise ValueError("Rate limited by Google (HTTP 429)")
            if "news.google" in final_url:
                raise ValueError("Failed to resolve original news URL")
            return final_url

        except Exception as e:
            raise Exception(f"Browser automation failed: {str(e)}")
        finally:
            browser.close()

google_news_url = "https://news.google.com/rss/articles/CBMipgFBVV95cUxPWV9fTEI4cjh1RndwanpzNVliMUh6czg2X1RjeEN0YUctUmlZb0FyeV9oT3RWM1JrMGRodGtqTk1zV3pkNEpmdGNxc2lfd0c4LVpGVENvUDFMOEJqc0FCVVExSlRrQmI3TWZ2NUc4dy1EVXF4YnBLaGZ4cTFMQXFFM2JpanhDR3hoRmthUjVjdm1najZsaFh4a3lBbDladDZtVS1FMHFn?oc=5"

print(get_correct_url(google_news_url))