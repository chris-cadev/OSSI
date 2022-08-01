from copyreg import constructor
from gc import callbacks
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import FormRequest, http, shell
import logging
import config


class FacebookLoginSpider(CrawlSpider):
    name = 'facebook login'
    allowed_domains = ['facebook.com']
    start_urls = ['http://www.facebook.com/login']

    csrf_token = None

    def cache_csrf_token(self, response):
        self.log(f'response login page: {response}', logging.DEBUG)

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formdata={
                'email': config.fb_user,
                'pass': config.fb_pass
            },
            callbacks=[self.logged_in]
        )

    def logged_in(self, response):
        self.log('Logged in!!', level=logging.DEBUG)
        pass
