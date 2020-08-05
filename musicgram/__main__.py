from typing import Union

from . import constants, last, spotify
from .telegram import MusicGramTelegramClient


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
        while True:
            track = client.get_current_track()
            if track.playing:
                LAST_NAME = f"[{track.title} - {track.artist}]"
                telegram.update_profile_photo(tg_client, track.cover)
                telegram.update_profile_last_name(tg_client, LAST_NAME)
                client.wait_for_new_track(track.id)
            else:
                telegram.update_profile_photo(tg_client)
                telegram.update_profile_last_name(
                    tg_client, "", constants.INITIAL_LAST_NAME)
                client.wait_for_track_play()

        print("Done waiting")


if __name__ == "__main__":
    main()
