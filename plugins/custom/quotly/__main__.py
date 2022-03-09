""" Quotli-ify."""

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import aiohttp
import json

from userge import userge, Message


class QuotlyException(Exception):
    pass


async def get_message_sender_id(msg: Message):
    if msg.forward_date:
        if msg.forward_sender_name:
            return 1
        elif msg.forward_from:
            return msg.forward_from.id
        elif msg.forward_from_chat:
            return msg.forward_from_chat.id
        else:
            return 1
    else:
        if msg.from_user:
            return msg.from_user.id
        elif msg.sender_chat:
            return msg.sender_chat.id
        else:
            return 1


async def get_message_sender_name(msg: Message):
    if msg.forward_date:
        if msg.forward_sender_name:
            return msg.forward_sender_name
        elif msg.forward_from:
            if msg.forward_from.last_name:
                return f"{msg.forward_from.first_name} {msg.forward_from.last_name}"
            else:
                return m.forward_from.first_name
        elif msg.forward_from_chat:
            return msg.forward_from_chat.title
        else:
            return ""
    else:
        if msg.from_user:
            if msg.from_user.last_name:
                return f"{msg.from_user.first_name} {msg.from_user.last_name}"
            else:
                return msg.from_user.first_name
        elif msg.sender_chat:
            return msg.sender_chat.title
        else:
            return ""


async def get_message_sender_username(msg: Message):
    if m.forward_date:
        if msg.forward_sender_name:
            return ""
        elif msg.forward_from:
            if msg.forward_from.username:
                return msg.forward_from.username
            else:
                return
        elif msg.forward_from_chat:
            if msg.forward_from_chat.username:
                return msg.forward_from_chat.username
            else:
                return ""
        else:
            return ""
    else:
        if msg.from_user:
            if msg.from_user.username:
                return msg.from_user.username
            else:
                return ""
        elif msg.sender_chat:
            if msg.sender_chat.username:
                return msg.sender_chat.username
            else:
                return ""
        else:
            return ""


async def get_message_sender_photo(msg: Message):
    if msg.forward_date:
        if msg.forward_sender_name:
            return ""
        elif msg.forward_from:
            if msg.forward_from.photo:
                return {
                    "small_file_id": m.forward_from.photo.small_file_id,
                    "small_photo_unique_id": m.forward_from.photo.small_photo_unique_id,
                    "big_file_id": m.forward_from.photo.big_file_id,
                    "big_photo_unique_id": m.forward_from.photo.big_photo_unique_id,
                }
            else:
                return ""
        elif msg.forward_from_chat:
            if msg.forward_from_chat.photo:
                return {
                    "small_file_id": msg.forward_from_chat.photo.small_file_id,
                    "small_photo_unique_id": msg.forward_from_chat.photo.small_photo_unique_id,
                    "big_file_id": msg.forward_from_chat.photo.big_file_id,
                    "big_photo_unique_id": msg.forward_from_chat.photo.big_photo_unique_id,
                }
            else:
                return ""
        else:
            return ""
    else:
        if msg.from_user:
            if msg.from_user.photo:
                return {
                    "small_file_id": msg.from_user.photo.small_file_id,
                    "small_photo_unique_id": msg.from_user.photo.small_photo_unique_id,
                    "big_file_id": msg.from_user.photo.big_file_id,
                    "big_photo_unique_id": msg.from_user.photo.big_photo_unique_id,
                }
            else:
                return ""
        elif msg.sender_chat:
            if msg.sender_chat.photo:
                return {
                    "small_file_id": msg.sender_chat.photo.small_file_id,
                    "small_photo_unique_id": msg.sender_chat.photo.small_photo_unique_id,
                    "big_file_id": msg.sender_chat.photo.big_file_id,
                    "big_photo_unique_id": msg.sender_chat.photo.big_photo_unique_id,
                }
            else:
                return ""
        else:
            return ""


async def get_text_or_caption(msg: Message):
    if msg.text:
        return msg.text
    elif msg.caption:
        return msg.caption
    else:
        return ""


async def pyrogram_to_quotly(messages):
    if not isinstance(messages, list):
        messages = [messages]
    payload = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1b1429",
        "messages": [],
    }

    for message in messages:
        the_message_dict_to_append = {}
        if message.entities:
            the_message_dict_to_append["entities"] = [
                {
                    "type": entity.type,
                    "offset": entity.offset,
                    "length": entity.length,
                }
                for entity in message.entities
            ]
        elif message.caption_entities:
            the_message_dict_to_append["entities"] = [
                {
                    "type": entity.type,
                    "offset": entity.offset,
                    "length": entity.length,
                }
                for entity in message.caption_entities
            ]
        else:
            the_message_dict_to_append["entities"] = []
        the_message_dict_to_append["chatId"] = await get_message_sender_id(message)
        the_message_dict_to_append["text"] = await get_text_or_caption(message)
        the_message_dict_to_append["avatar"] = True
        the_message_dict_to_append["from"] = {}
        the_message_dict_to_append["from"]["id"] = await get_message_sender_id(message)
        the_message_dict_to_append["from"]["name"] = await get_message_sender_name(message)
        the_message_dict_to_append["from"]["username"] = await get_message_sender_username(message)
        the_message_dict_to_append["from"]["type"] = message.chat.type
        the_message_dict_to_append["from"]["photo"] = await get_message_sender_photo(message)
        if message.reply_to_message:
            the_message_dict_to_append["replyMessage"] = {
                "name": await get_message_sender_name(message.reply_to_message),
                "text": await get_text_or_caption(message.reply_to_message),
                "chatId": await get_message_sender_id(message.reply_to_message),
            }
        else:
            the_message_dict_to_append["replyMessage"] = {}
        payload["messages"].append(the_message_dict_to_append)
    async with aiohttp.ClientSession() as ses:
        data = await ses.post(f"https://bot.lyo.su/quote/generate.png", json=payload)
        if not data.is_error:
            return data.read()
        else:
            raise QuotlyException(data.json())


def isArgInt(txt) -> list:
    count = txt
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@userge.on_cmd(
    "q",
    about={
        "header": "Quotly-ify a nice quote",
        "description": "Make an quote sticker like a Quotly.",
        "usage": "{tr}q [reply to message]",
    },
)
async def quotly_cmd(msg: Message):
    if len(msg.text.split()) > 1:
        check_arg = isArgInt(msg.command[1])
        if check_arg[0]:
            if check_arg[1] < 2 or check_arg[1] > 10:
                return await msg.reply_text("`Invalid range of message..`")
            else:
                try:
                    messages = [
                        i
                        for i in await message.client.get_messages(
                            chat_id=msg.chat.id,
                            message_ids=range(
                                msg.reply_to_message.message_id,
                                msg.reply_to_message.message_id + (check_arg[1] + 5),
                            ),
                            replies=-1,
                        )
                        if not i.empty and not i.media
                    ]
                except:
                    return await msg.reply_text("¯\\_(ツ)_/¯")
                try:
                    make_quotly = await pyrogram_to_quotly(messages)
                    bio_sticker = BytesIO(make_quotly)
                    bio_sticker.name = "biosticker.webp"
                    return await msg.reply_sticker(bio_sticker)
                except:
                    return await msg.reply_text("¯\\_(ツ)_/¯")
        else:
            pass
    try:
        messages_one = await message.client.get_messages(
            chat_id=msg.chat.id, message_ids=msg.reply_to_message.message_id, replies=-1
        )
        messages = [messages_one]
    except:
        return await msg.reply_text("¯\\_(ツ)_/¯")
    try:
        make_quotly = await pyrogram_to_quotly(messages)
        bio_sticker = BytesIO(make_quotly)
        bio_sticker.name = "biosticker.webp"
        return await msg.reply_sticker(bio_sticker)
    except:
        return await msg.reply_text("¯\\_(ツ)_/¯")
