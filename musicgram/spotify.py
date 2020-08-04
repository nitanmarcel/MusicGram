from spotipy import Spotify, SpotifyOAuth


class Client:
    def __init__(
            self,
            api_id: str,
            api_secret: str,
            redirect_uri: str) -> None:
        self.client_id = api_id
        self.client_secret = api_secret
        self.redirect_uri = redirect_uri

    @property
    def client(self):
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-read-currently-playing",
            username="spotyton")
        return Spotify(auth_manager=auth_manager)
