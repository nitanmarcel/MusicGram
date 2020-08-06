import logging
import time
from io import BytesIO
from typing import Union

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)

from musicgram.db import DataBase

LOGGER = logging.getLogger(__name__)


class MusicGramTelegramClient:
    def __init__(self, api_id: str, api_hash: str, regenerate_db: bool = False):
        self.id = api_id
        self.hash = api_hash
        self._client: TelegramClient = None


    @property
    def client(self) -> TelegramClient:
        self._client =  TelegramClient("musicgram", self.id, self.hash)
        return self._client

    def update_profile_photo(
            self,
            client: TelegramClient,
            file: BytesIO = None,
           initial_photo_len: int = 0) -> None:
        try:
            pictures = client.get_profile_photos("me")
            if file:
                client(
                    UploadProfilePhotoRequest(
                        file=client.upload_file(file=file, file_name="cover.jpg")
                    )
                )
            if pictures.total > initial_photo_len:
                client(DeletePhotosRequest([pictures[0]]))

        except FloodWaitError as exception:
            LOGGER.INFO(
                f"UploadProfilePhotoRequest flood error pausing for {exception.seconds} seconds!")
            time.sleep(exception.seconds)

    def update_profile_last_name(self,
                                 client: TelegramClient,
                                 last_name: Union[str,
                                                  None] = None) -> None:
        try:
            client(UpdateProfileRequest(last_name=last_name))
        except FloodWaitError as exception:
            LOGGER.INFO(
                f"UpdateProfileRequest flood error pausing for {exception.seconds} seconds!")
            time.sleep(exception.seconds)

    def save_profile(self):
        if self._client is not None:
            db = DataBase(self._client)
            me = self._client.get_me()
            last_name = me.last_name or ""
            profile_pics = len(self._client.get_profile_photos("me"))
            data = db.generate((last_name, profile_pics))
            db.save()
            return data