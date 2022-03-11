"""Slap."""

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


@userge.on_cmd(
    "slap",
    about={
        "header": "slap user using neko gif.",
        "description": "Slaping user with randomly gif from neko.",
        "usage": "{tr}slap [reply to message]",
    },
)
async def _slap(msg: Message):
    """Slap handler, will return url."""
    if not msg.reply_to_message:
        return await msg.edit("__who will i slap?__")

    async with aiohttp.ClientSession() as ses:
        async with ses.get("https://www.nekos.life/api/v2/img/slap") as nf:
            if nf.status != 200:
                return await message.edit("__Something went wrong..__")
            else:
                return await message.reply_to_message.reply_animation(data["url"])
