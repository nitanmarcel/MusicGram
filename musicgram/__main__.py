import time
from typing import Union

from . import constants, last, spotify, utils
from .telegram import MusicGramTelegramClient


def main():
    if constants.USE_SPOTIFY:
        client: Union[last.Client, spotify.Client] = spotify.Client(
            api_id=constants.API_KEY,
            api_secret=constants.API_SECRET,
            redirect_uri=constants.REDIRECT_URI)
    else:
        client: Union[last.Client, spotify.Client] = last.Client(
            api_key=constants.API_KEY,
            api_secret=constants.API_SECRET)

    telegram = MusicGramTelegramClient(
        api_id=constants.API_ID,
        api_hash=constants.API_HASH)
    with telegram.client as tg_client:
        while True:
            track = utils.get_current_track(client, constants.USERNAME)
            if track.playing:
                LAST_NAME = f"[{track.title} - {track.artist}]"
                telegram.update_profile_photo(tg_client, track.cover)
                telegram.update_profile_last_name(tg_client, LAST_NAME)
                utils.wait_for_next_track(
                    client,
                    constants.USERNAME,
                    track.id,
                    update_time=constants.UPDATE_TIME)
            else:
                telegram.update_profile_photo(tg_client)
                telegram.update_profile_last_name(
                    tg_client, "", constants.INITIAL_LAST_NAME)
                while not track.playing:
                    track = utils.get_current_track(client, constants.USERNAME)
                    time.sleep(constants.UPDATE_TIME)


if __name__ == "__main__":
    main()
