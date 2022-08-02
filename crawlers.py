import re
import config as config
from playwright.sync_api import sync_playwright, Page, Browser
import utils
import config

DEFAULT_RELATIVES_CRAWL_DEPTH = 3


class FacebookCrawler():
    def login(self, browser: Browser):
        page = browser.new_page()
        page.goto(
            'http://www.facebook.com/login',
            wait_until='networkidle'
        )
        if 'login' in page.url:
            form = page.locator('//*/form').first
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
        cookies = browser.cookies(urls=['https://www.facebook.com'])
        utils.save_object(cookies, '.session/cookies.json')
        page.close()
        # TODO: add method to insert the cookies in the browser


class FacebookProfileCrawler(FacebookCrawler):
    def download_profile_picture(self, page, profile_view_url: str):
        page.goto(
            profile_view_url,
            wait_until='networkidle'
        )
        profile_picture_url = page.locator(
            '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img'
        ).get_attribute('src')
        return utils.save_url_picture(
            profile_picture_url,
            '.session/profile/picture.jpg'
        )

    def find_profile_id(self, page: Page):
        json_scripts = page.locator(
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

    def download_data(self, profile_url):
        print(f'downloading data from: {profile_url}')
        with sync_playwright() as playwright_api:
            browser = playwright_api.chromium.launch_persistent_context(
                '.browser', headless=True
            )
            self.login(browser)
            page = browser.new_page()
            page.goto(
                profile_url,
                wait_until='networkidle'
            )

            print('getting profile id...')
            profile_id = self.find_profile_id(page)
            print(f'profile id: {profile_id}')

            print('getting name...')
            name = page.locator(
                '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/div/h1'
            ).first.inner_text()
            print(f'name: {name}')

            print('getting profile picture...')
            page.locator(
                '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div'
            ).click()
            profile_picture_fb_view_url = page.locator(
                '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/a'
            ).get_attribute('href')
            profile_picture_filename = self.download_profile_picture(
                page,
                profile_picture_fb_view_url
            )
            print(f'profile picture filename: {profile_picture_filename}')

            return {
                "ID": profile_id,
                "name": name,
                "picture": profile_picture_filename,
                "url": profile_url,
            }


class FacebookFriendCrawler(FacebookCrawler):
    def download_relative(self):
        pass
