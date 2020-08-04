import requests


class Track(object):
    def __init__(
            self,
            id=None,
            title=None,
            artist=None,
            cover=None,
            playing=False):
        self.id = id
        self.title = title
        self.artist = artist
        self.cover = self._get_cover(cover)
        self.playing = playing

    @staticmethod
    def _get_cover(cover_uri):
        if cover_uri:
            return requests.get(cover_uri).content
