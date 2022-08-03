
from playwright.sync_api import sync_playwright, Page, Browser


class PlaywrigthWrapper():
    Instance = None

    @staticmethod
    def get_instance():
        if PlaywrigthWrapper.Instance is None:
            PlaywrigthWrapper.Instance = PlaywrigthWrapper()
        return PlaywrigthWrapper.Instance

    def __init__(self) -> None:
        self.headless = False
        self.browser_path = '.browser'
        self.api = sync_playwright().start()
        self.browser = self.api.chromium.launch_persistent_context(
            self.browser_path, headless=self.headless
        )
        self.page = self.browser.new_page()

    def goto(self, url: str):
        if self.page is None or self.page.url == url:
            return self.page
        self.page.goto(url, wait_until='networkidle')
        return self.page

    def close(self):
        self.browser.close()
