import time

from spotipy import Spotify, SpotifyOAuth

from musicgram.types import Track


class Client:
    def __init__(
            self,
            api_id: str,
            api_secret: str,
            redirect_uri: str,
            username: str,
            update_time: int) -> None:
        self.client_id = api_id
        self.client_secret = api_secret
        self.redirect_uri = redirect_uri
        self.username = username
        self.update_time = update_time
        self._client: Spotify = None

    def init(self):
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-read-currently-playing",
            username=self.username)
        self._client = Spotify(auth_manager=auth_manager)
        return self._client

    def get_current_track(self):
        track = self._client.current_user_playing_track()
        if not track:
            return Track()
        song = track['item']
        return Track(
            song['id'],
            song['name'],
            song['artists'][0]['name'],
            song['album']['images'][0]['url'],
            track['is_playing']
        )

    def wait_for_new_track(self, last_track_id):
        track = self.get_current_track()
        while track.playing and track.id == last_track_id:
            time.sleep(self.update_time)
            track = self.get_current_track()

    def wait_for_track_play(self):
        track = self.get_current_track()
        while not track.playing:
            time.sleep(self.update_time)
            track = self.get_current_track()