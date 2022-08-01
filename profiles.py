from copyreg import constructor
from crawlers import FacebookProfileCrawler


class Profile:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)
        self.ID = kwargs.get('ID', None)
        self.name = kwargs.get('name', None)
        self.picture = kwargs.get('picture', None)

    def get_relatives() -> list:
        pass


class FacebookProfile(Profile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.friends = kwargs.get('friends', [])


class ProfileFactory:
    def create_profile(self, url: str) -> Profile:
        if 'facebook' in url:
            data = FacebookProfileCrawler.download_data(url)
            return FacebookProfile(
                url=data.get('url', None),
                ID=data.get('ID', None),
                name=data.get('name', None),
                picture=data.get('picture', None),
                friends=data.get('friends', [])
            )
        if 'instagram' in url:
            raise NotImplementedError(
                'instagram data extraction not implemented yet'
            )
        if 'twitter' in url:
            raise NotImplementedError(
                'twitter data extraction not implemented yet'
            )
        if 'twitch' in url:
            raise NotImplementedError(
                'twitch data extraction not implemented yet'
            )
        if 'youtube' in url:
            raise NotImplementedError(
                'youtube data extraction not implemented yet'
            )

    def download_relatives_from_profile(self, profile: Profile) -> list:
        return []
        # if not issubclass(profile, Profile):
        #     return None

        # if isinstance(profile, FacebookProfile):
        #     factory = FacebookProfileCrawler.download_relatives()

        # if factory is None:
        #     return []

        # return factory.download_relatives_from_profile(profile)
