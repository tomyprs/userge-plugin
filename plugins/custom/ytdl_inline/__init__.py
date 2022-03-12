"""ytdl inline features."""

from uuid import uuid4
from typing import Optional

def rand_key():
    return str(uuid4())[:8]

def check_owner(func):
    async def wrapper(_, c_q: CallbackQuery):
        if c_q.from_user and (
            c_q.from_user.id in Config.OWNER_ID or c_q.from_user.id in Config.SUDO_USERS
        ):
            try:
                await func(c_q)
            except FloodWait as e:
                await asyncio.sleep(e.x + 5)
            except MessageNotModified:
                pass
        else:
            await c_q.answer(
                "You doesn't have permission",
                show_alert=True,
            )
        return wrapper

# https://www.tutorialspoint.com/How-do-you-split-a-list-into-evenly-sized-chunks-in-Python
def sublists(input_list: list, width: int = 3):
    return [input_list[x : x + width] for x in range(0, len(input_list), width)]

def get_file_id(
    message: "userge.Message",
) -> Optional[str]:
    """get file_id"""
    if message is None:
        return
    file_ = (
        message.audio
        or message.animation
        or message.photo
        or message.sticker
        or message.voice
        or message.video_note
        or message.video
        or message.document
    )
    return file_.file_id if file_ else None
