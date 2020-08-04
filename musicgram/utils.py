import time
from typing import Union

from . import last, spotify
from .types import Track


def get_current_track(client: Union[last.Client,
                                    spotify.Client],
                      username: Union[str,
                                      None] = None) -> Union[Track,
                                                             None]:
    if isinstance(client, spotify.Client):
        track = client.client.current_user_playing_track()
        if not track:
            return Track()
        item = track['item']
        return Track(
            item['id'],
            item['name'],
            item['artists'][0]['name'],
            item['album']['images'][0]['url'],
            track['is_playing'])

    user = client.client.get_user(username)
    playing = user.get_now_playing()
    if not playing:
        return Track()
    id = str(hash(playing.title + playing.artist.get_name()))[1:13]
    covers = playing.info['image']
    return Track(id, playing.title, playing.artist.get_name(),
                 covers[len(covers) - 1] if covers else None, True)


def wait_for_next_track(client: Union[last.Client,
                                      spotify.Client],
                        username: str,
                        last_track_id: Union[str,
                                             None],
                        update_time: int):
    track = get_current_track(client, username)
    while track.playing and track.id == last_track_id:
        track = get_current_track(client)
        time.sleep(update_time)
