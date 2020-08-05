import time

import pylast
import requests

from musicgram.types import Track


class Client:
    def __init__(self, api_key: str, api_secret: str,
                 username: str, update_time):
        self.api_key = api_key
        self.api_secret = api_secret
        self.username = username
        self.update_time = update_time
        self._client: pylast.LastFMNetwork = None

    def init(self):
        self._client = pylast.LastFMNetwork(
            api_key=self.api_key,
            api_secret=self.api_secret,
            username=self.username)
        self._client.enable_caching()
        return self._client

    def get_current_track(self):
        r = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={self.username}&limit=1&api_key={self.api_key}&format=json")
        if r.status_code in [200, 201]:
            json = r.json()
            track = json['recenttracks']['track'][0]
            artist = track['artist']['#text']
            title = track['name']

            cover = self._client.get_album(artist, title).get_cover_image(size=pylast.SIZE_MEGA) or \
                self._client.get_album(artist, title).get_cover_image(size=pylast.SIZE_EXTRA_LARGE) or \
                self._client.get_album(artist, title).get_cover_image(size=pylast.SIZE_LARGE) or \
                self._client.get_album(artist, title).get_cover_image(size=pylast.SIZE_MEDIUM) or \
                track['image'][3]

            playing = False

            if '@attr' in track.keys():
                playing = track['@attr']['nowplaying']
            id = self._client.get_track(artist, title).get_mbid()
            return Track(id, title, artist, cover, playing)
        return Track()

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
