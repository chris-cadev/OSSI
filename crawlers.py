import re
import config as config
from playwright.sync_api import sync_playwright, Page, Browser
import utils
import config

DEFAULT_RELATIVES_CRAWL_DEPTH = 3


class FacebookCrawler():
    page: Page = None
    browser: Browser = None
    browser_path = '.browser'
    session_path = '.session'

    def login(self, profile_url: str):
        user_id = utils.remove_domain(profile_url)
        browser_api = sync_playwright().start()
        self.browser = browser_api.chromium.launch_persistent_context(
            self.browser_path, headless=True
        )
        self.page = self.browser.new_page()
        self.goto('http://www.facebook.com/login')
        if 'login' in self.page.url:
            form = self.page.locator('//*/form').first
            container = form.locator('//div')
            email_input = container.locator("//*/input[@id='email']").first
            passwd_input = container.locator("//*/input[@id='pass']").first
            login_button = form.locator(
                '//*/*[@id="loginbutton"]'
            ).first
            email_input.fill(config.fb_user)
            passwd_input.fill(config.fb_pass)
            login_button.click()
            utils.wait('once you are in your "feed" press [ENTER]')
        cookies = self.browser.cookies(urls=['https://www.facebook.com'])
        utils.save_object(
            cookies, f'{self.session_path}/{user_id}-cookies.json'
        )
        self.page.close()

    def goto(self, url: str):
        if self.page is None or self.page.url == url:
            return self.page
        self.page.goto(url, wait_until='networkidle')
        return self.page

    def close(self):
        if self.browser is None:
            return
        self.browser.close()


class FacebookProfileCrawler(FacebookCrawler):
    def download_data(self, profile_url: str):
        print(f'downloading data from: {profile_url}')
        self.login(profile_url)
        self.page = self.browser.new_page()
        self.goto(profile_url)

        print('getting profile id...')
        profile_id = self.find_profile_id()
        print(f'profile id: {profile_id}')

        print('getting name...')
        name = self.get_name()
        print(f'name: {name}')

        print('getting profile picture...')
        profile_picture_url = self.get_profile_picture_url()
        print(f'profile picture url: {profile_picture_url}')

        print(f'downloading profile picture of {profile_url}')
        profile_picture_path = self.save_profile_picture(
            profile_picture_url, profile_url
        )
        print('profile picture downloaded!')

        return {
            "ID": profile_id,
            "name": name,
            "picture": profile_picture_path,
            "url": profile_url,
        }

    def get_profile_picture_url(self):
        self.page.locator(
            '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div'
        ).click()
        profile_view_url = self.page.locator(
            '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/a'
        ).get_attribute('href')
        self.goto(profile_view_url)
        profile_picture_url = self.page.locator(
            '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img'
        ).get_attribute('src')
        return profile_picture_url

    def save_profile_picture(self, picture_url: str, profile_url: str):
        profile_picture_filename = utils.remove_domain(profile_url)
        profile_picture_path = f'{self.session_path}/profile-picture/{profile_picture_filename}.jpg'
        utils.save_url_picture(
            picture_url,
            profile_picture_path
        )
        return profile_picture_path

    def find_profile_id(self):
        json_scripts = self.page.locator(
            '//html/body/script[@type="application/json"]').element_handles()
        for script in json_scripts:
            json_text = script.inner_text()
            if '"profile_id"' in json_text:
                match = re.search(
                    "\"profile_id\":[0-9]+", json_text
                )
                if match is not None:
                    return match.group().split(":")[1]
        return None

    def get_name(self):
        return self.page.locator(
            '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/div/h1'
        ).first.inner_text()


class FacebookFriendCrawler(FacebookCrawler):
    def download_relative(self):
        pass
