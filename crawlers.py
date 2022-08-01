import config as config
from playwright.sync_api import sync_playwright
import utils
import config

DEFAULT_RELATIVES_CRAWL_DEPTH = 3


class FacebookProfileCrawler():
    @staticmethod
    def download_profile_picture(page, profile_view_url: str):
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

    @staticmethod
    def download_data(url):
        with sync_playwright() as playwright_api:
            browser = playwright_api.chromium.launch_persistent_context(
                '.browser', headless=False
            )
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
                print('once you are in your feed press [ENTER]')
                utils.wait()
            cookies = browser.cookies(urls=['https://www.facebook.com'])
            utils.save_object(cookies, '.session/cookies.json')
            profile_button = page.locator(
                '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div[1]/ul/li/div/a'
            ).first
            profile_url = profile_button.get_attribute('href')
            page.goto(
                profile_url,
                wait_until='networkidle'
            )
            page.locator(
                '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div'
            ).click()
            profile_picture_fb_view_url = page.locator(
                '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/a'
            ).get_attribute('href')
            profile_picture_filename = FacebookProfileCrawler.download_profile_picture(
                page,
                profile_picture_fb_view_url
            )
            return {
                "ID": None,
                "name": None,
                "picture": profile_picture_filename,
                "url": url,
            }

    @staticmethod
    def download_relatives(depth: int = DEFAULT_RELATIVES_CRAWL_DEPTH):
        pass
