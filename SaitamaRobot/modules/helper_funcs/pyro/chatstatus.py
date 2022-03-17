from pyrogram.types import Message

from SaitamaRobot.modules.helper_funcs.pyro import IMMUNE_USERS
from SaitamaRobot import SUPPORT_USERS

ADMIN_STATUS = frozenset(["adminstrator", "creator"])


async def is_user_admin(message: Message):
    if message.chat.type == "private" or message.from_user.id in SUPPORT_USERS:
        return True
    if member := await message.chat.get_member(message.from_user.id):
        return member.status in ADMIN_STATUS


async def is_bot_admin(chat_id: int):
    bot = await pyro.get_me()
    if member := await pyrogram_app.get_chat_member(chat_id, bot.id):
        return member.status in ADMIN_STATUS


async def is_user_in_chat(message: Message):
    if await member.get_member(message.from_user.id):
        return True


async def can_change_info(message: Message):
    if member := await message.chat.get_member(message.from_user.id):
        return member.can_change_info


async def can_ban_users(message: Message):
    if member := await message.chat.get_member(message.from_user.id):
        return member.can_ban_users


async def can_pin_messages(message: Message):
    if member := await message.chat.get_member(message.from_user.id):
        return member.pin_messages


async def can_invite_users(message: Message):
    if member := await message.chat.get_member(message.from_user.id):
        return member.can_invite_users


async def can_add_admins(message: Message):
    if member := await message.chat.get_member(message.from_user.id):
        return member.can_add_admins


async def can_delete_messages(message: Message):
    if message.chat.type == "private":
        return True
    if member := await message.chat.get_member(message.from_user.id):
        return member.can_delete_messages
