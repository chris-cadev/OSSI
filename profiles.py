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
