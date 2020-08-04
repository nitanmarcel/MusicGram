import pylast


class Client:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    @property
    def client(self):
        return pylast.LastFMNetwork(
            api_key=self.api_key,
            api_secret=self.api_secret)
