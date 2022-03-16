import html

from pyrogram import Client, filters
from pyrogram.types import Message, Chat, User

from SaitamaRobot import PREFIX, DEV_USERS, pyrogram_app
from SaitamaRobot.__main__ import STATS
from SaitamaRobot.modules.sql import afk_sql
from SaitamaRobot.modules.helper_funcs.pyro.entities import (
    iter_user_entities,
    iter_chat_entities,
)

# TODO: switch to aiogram later


@pyrogram_app.on_message(filters.command("id", PREFIX))
async def get_id(_: Client, msg: Message) -> None:
    async for user in iter_user_entities(msg):
        if user:
            await msg.reply_text(f"{user.first_name}'s id is <code>{user.id}</code>")
            return

    if msg.reply_to_message and (user := msg.reply_to_message.from_user):
        await msg.reply_text(f"{user.first_name}'s id is <code>{user.id}</code>")
    elif msg.chat.type == "private":
        await msg.reply_text(f"Your id is <code>{msg.chat.id}</code>.")
    else:
        await msg.reply_text(f"This group's id is <code>{msg.chat.id}</code>.")


def ginfo_text(chat: Chat) -> str:
    text = (
        f"<b>ID</b>: <code>{chat.id}</code>"
        f"\n<b>Title</b>: {chat.title}"
        f"\n<b>Type</b>: {chat.type}"
    )

    if chat.username:
        text += f"\n<b>Username</b>: @{chat.username}"
    if chat.invite_link:
        text += f"\n<b>Invitelink</b>: {chat.invite_link}"

    text += (
        f"\n<b>Member Count</b>: {chat.members_count}"
        f"\n<b>Datacenter</b>: {chat.dc_id}"
        f"\n<b>Protected Content</b>: {chat.has_protected_content}"
    )

    if chat.is_verified:
        text += f"\n<b>Verified</b>: {chat.is_verified}"
    if chat.is_restricted:
        text += f"\n<b>Restricted</b>: {chat.is_restricted}"
    if chat.is_scam:
        text += f"\n<b>Scam</b>: {chat.is_scam}"
    if chat.is_fake:
        text += f"\n<b>Fake</b>: {chat.is_fake}"

    text += f"\n<b>ChatPermissions</b>:\n{chat.permissions}"

    return text


@pyrogram_app.on_message(
    filters.command("ginfo", PREFIX) & filters.user(list(DEV_USERS))
)
async def group_info(_: Client, msg: Message) -> None:
    # Can use aioitertools.chain(iter_chat_entities(msg), [msg.chat])
    async for chat in iter_chat_entities(msg):
        if chat:
            await msg.reply_text(ginfo_text(chat))
            return

    await msg.reply_text(ginfo_text(msg.chat))


def info_text(user: User) -> str:
    text = (
        f"<b>ID</b>: <code>{user.id}</code>"
        f"\n<b>First Name</b>: {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n<b>Last Name</b>: {html.escape(user.last_name)}"
    if user.username:
        text += f"\n<b>Username</b>: @{html.escape(user.username)}"

    text += (
        f"\n<b>link</b>: {user.mention(style='html')}"
        f"\n<b>AFK</b>: {afk_sql.is_afk(user.id)}"
    )

    return text


@pyrogram_app.on_message(filters.command("info", PREFIX))
async def info(_: Client, msg: Message) -> None:
    async for user in iter_user_entities(msg):
        if user:
            await msg.reply_text(info_text(user))
            return

    if msg.reply_to_message:
        await msg.reply_text(info_text(msg.reply_to_message.from_user))
    else:
        await msg.reply_text(info_text(msg.from_user))


@pyrogram_app.on_message(
    filters.command("stats", PREFIX) & filters.user(list(DEV_USERS))
)
async def stats(_: Client, msg: Message) -> None:
    await msg.reply_text(
        "<b>Current stats:</b>\n" + "\n".join(mod.__stats__() for mod in STATS)
    )


__help__ = """
*ID:*
 • `/id`*:* get the current group id. If used by replying to a message, gets that user's id.
*Overall Information about you:*
 • `/info`*:* get information about a user.

"""


__mod_name__ = "Info"
