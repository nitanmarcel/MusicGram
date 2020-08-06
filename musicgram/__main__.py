import re
from typing import Union

from . import constants, last, spotify
from .telegram import MusicGramTelegramClient


def trim(artist, title):
    res = f"[{title} - {artist}]"
    if len(res) > 59:
        if round(len(title) / 2) + len(" - ") + len(artist) < 59:
            trim_len = round(len(title) / 2)
            title = title[:trim_len] + "..."
            return f"[{title} - {artist}]"
        elif len(title) + len(" - ") + round(len(artist) / 2) < 59:
            trim_len = round(len(artist) / 2)
            artist = artist[:trim_len] + "..."
            return f"[{title} - {artist}]"
    else:
        return res


def main():
    if constants.USE_SPOTIFY:
        client: Union[last.Client, spotify.Client] = spotify.Client(
            api_id=constants.API_KEY,
            api_secret=constants.API_SECRET,
            redirect_uri=constants.REDIRECT_URI,
            username=constants.USERNAME,
            update_time=constants.UPDATE_TIME)
    else:
        client: Union[last.Client, spotify.Client] = last.Client(
            api_key=constants.API_KEY,
            api_secret=constants.API_SECRET,
            username=constants.USERNAME,
            update_time=constants.UPDATE_TIME)

    telegram = MusicGramTelegramClient(
        api_id=constants.API_ID,
        api_hash=constants.API_HASH)
    with telegram.client as tg_client:
        client.init()
        initial_last_name, len_profile_photos = telegram.save_profile()
        while True:
            track = client.get_current_track()
            if track.playing:
                new_last_name = trim(track.artist, track.title)
                telegram.update_profile_photo(tg_client, track.cover, len_profile_photos)
                telegram.update_profile_last_name(tg_client, new_last_name)
                client.wait_for_new_track(track.id)
            else:
                telegram.update_profile_photo(tg_client, initial_photo_len=len_profile_photos)
                telegram.update_profile_last_name(tg_client, initial_last_name)
                client.wait_for_track_play()



if __name__ == "__main__":
    main()
