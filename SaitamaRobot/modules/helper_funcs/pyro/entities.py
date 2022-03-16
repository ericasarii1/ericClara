from pyrogram.types import Message

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
                yield await pyrogram_app.get_users(userid)


async def iter_chat_entities(msg: Message):
    """Get chats from message entities"""
    for entity in msg.entities:
        match entity.type:
            case "mention" | "phone_number":
                chatid = msg.text[entity.offset : entity.offset + entity.length]
                yield await pyrogram_app.get_chat(chatid)
