
import json
from crawlers import FacebookFriendCrawler, FacebookProfileCrawler
from profiles import FacebookProfile, Profile


class RelationFactory:
    def generate_relation(self, parent, child):
        return {
            "source": f'{parent}',
            "target": f'{child}'
        }

    def generate_relations(self, parent, children):
        relations = []
        for child in children:
            relation = self.generate_relation(parent, child)
            relations.append(relation)

        return relations


class ProfileFactory:
    def create_profile_from_url(self, url: str) -> Profile:
        if 'facebook' in url:
            crawler = FacebookProfileCrawler()
            data = crawler.download_data(url)
            return FacebookProfile(
                url=data.get('url', None),
                ID=data.get('ID', None),
                name=data.get('name', None),
                picture=data.get('picture', None)
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

    def create_profile_from_json(self, filename: str):
        with open(filename, 'r') as f:
            data = json.loads(f.read())
            if 'facebook' in f"{data.get('class_name', '')}".lower():
                return FacebookProfile(
                    url=data.get('url', None),
                    ID=data.get('ID', None),
                    name=data.get('name', None),
                    picture=data.get('picture', None)
                )

    def download_relatives_from_profile(self, profile: Profile) -> list:
        if not issubclass(profile.__class__, Profile):
            return None

        if isinstance(profile, FacebookProfile):
            crawler = FacebookFriendCrawler()

        # if factory is None:
        #     return []

        # return factory.download_relatives_from_profile(profile)
        return crawler.download_relatives(profile)
