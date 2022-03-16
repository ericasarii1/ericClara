from contextlib import suppress

from pyrogram.types import Message
from pyrogram.errors import UsernameNotOccupied, PeerIdInvalid


from SaitamaRobot import pyrogram_app

# TODO: client kwarg


async def iter_user_entities(msg: Message):
    """Get users from message entities"""
    for entity in msg.entities:
        match entity.type:

            case "text_mention":
                yield entity.user

            case "mention" | "phone_number":
                userid = msg.text[entity.offset : entity.offset + entity.length]
                with suppress([UsernameNotOccupied, PeerIdInvalid]):
                    yield await pyrogram_app.get_users(userid)

            case "url":
                user_url = msg.text[entity.offset : entity.offset + entity.length]

                with suppress([UsernameNotOccupied, PeerIdInvalid]):
                    if user_url.startswith("https://t.me/"):
                        username = "@" + user_url.removeprefix("https://t.me/")
                        yield await pyrogram_app.get_chat(username)
                    elif user_url.startswith("t.me/"):
                        username = "@" + user_url.removeprefix("t.me/")
                        yield await pyrogram_app.get_chat(username)


async def iter_chat_entities(msg: Message):
    """Get chats from message entities"""
    for entity in msg.entities:
        match entity.type:

            case "mention" | "phone_number":
                chatid = msg.text[entity.offset : entity.offset + entity.length]
                with suppress([UsernameNotOccupied, PeerIdInvalid]):
                    yield await pyrogram_app.get_chat(chatid)

            case "url":
                chat_url = msg.text[entity.offset : entity.offset + entity.length]

                with suppress([UsernameNotOccupied, PeerIdInvalid]):
                    if chat_url.startswith("https://t.me/"):
                        path = chat_url.removeprefix("https://t.me/")
                        if not (path.startswith("joinchat") or path.startswith("+")):
                            username = "@" + path
                            yield await pyrogram_app.get_chat(username)

                    elif chat_url.startswith("t.me/"):
                        path = chat_url.removeprefix("t.me/")
                        if not (path.startswith("joinchat") or path.startswith("+")):
                            username = "@" + path
                            yield await pyrogram_app.get_chat(username)
