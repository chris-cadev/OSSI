import re
import time
import config as config
from profiles import FacebookProfile
import utils
import config
from wrappers import PlaywrigthWrapper
from playwright.sync_api import Request

DEFAULT_RELATIVES_CRAWL_DEPTH = 3


class FacebookCrawler():

    def __init__(self) -> None:
        playwright = PlaywrigthWrapper.get_instance()
        self.browser = playwright.browser
        self.page = playwright.page
        self.session_path = '.session'

    def login(self, profile_url: str):
        user_id = utils.remove_domain(profile_url)
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

    def goto(self, url: str):
        PlaywrigthWrapper.get_instance().goto(url)


class FacebookProfileCrawler(FacebookCrawler):
    def download_data(self, profile_url: str):
        print(f'downloading data from: {profile_url}')
        self.login(profile_url)
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

    def infinite_scroll(self):
        self.page.evaluate(
            """
            var intervalID = setInterval(function () {
                var scrollingElement = (document.scrollingElement || document.body);
                scrollingElement.scrollTop = scrollingElement.scrollHeight;
            }, 200);

            """
        )
        prev_height = None
        while True:
            curr_height = self.page.evaluate(
                '(window.innerHeight + window.scrollY)')
            if not prev_height:
                prev_height = curr_height
                time.sleep(1)
            elif prev_height == curr_height:
                self.page.evaluate('clearInterval(intervalID)')
                break
            else:
                prev_height = curr_height
                time.sleep(1)

    def download_relatives(self, profile: FacebookProfile):
        self.goto(f'{profile.url}/friends')
        self.infinite_scroll()
        friend_boxes = self.page.locator(
            '//html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div'
        )
        # TODO: probably use beautifull soup from here https://www.crummy.com/software/BeautifulSoup/bs4/doc/

        friends = []
        for i in range(friend_boxes.count()):
            box = friend_boxes.nth(i)
            link_tag = box.locator('//div[2]/div[1]/a').first
            image_tag = box.locator('//div[1]/a/img').first

            profile_url = link_tag.get_attribute('href')
            name = link_tag.inner_text()
            picture_url = image_tag.get_attribute('src')
            friends.append({
                "url": profile_url,
                "name": name,
                "picture": picture_url,
            })
        return friends
