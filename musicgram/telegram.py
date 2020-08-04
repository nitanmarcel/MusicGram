import logging
import time
from io import BytesIO
from typing import Union

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)

LOGGER = logging.getLogger(__name__)


class MusicGramTelegramClient:
    def __init__(self, api_id: str, api_hash: str):
        self.id = api_id
        self.hash = api_hash

    @property
    def client(self) -> TelegramClient:
        return TelegramClient("musicgram", self.id, self.hash)

    def update_profile_photo(
            self,
            client: TelegramClient,
            file: BytesIO = None) -> None:
        try:
            pictures = client.get_profile_photos("me")
            if file:
                client(
                    UploadProfilePhotoRequest(
                        file=client.upload_file(
                            file=file,
                            file_name="cover.jpg")))
            if pictures and len(pictures) > 1:
                client(DeletePhotosRequest([pictures[0]]))
        except FloodWaitError as exception:
            LOGGER.INFO(
                f"UploadProfilePhotoRequest flood error pausing for {exception.seconds} seconds!")
            time.sleep(exception.seconds)

    def update_profile_last_name(self,
                                 client: TelegramClient,
                                 last_name: Union[str,
                                                  None] = None,
                                 initial_last_name: str = "") -> None:
        try:
            if not last_name:
                client(UpdateProfileRequest(last_name=initial_last_name))
            else:
                client(UpdateProfileRequest(last_name=last_name))
        except FloodWaitError as exception:
            LOGGER.INFO(
                f"UpdateProfileRequest flood error pausing for {exception.seconds} seconds!")
            time.sleep(exception.seconds)
