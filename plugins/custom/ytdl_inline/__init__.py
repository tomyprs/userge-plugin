"""ytdl inline features."""

from uuid import uuid4
from typing import Optional
from html_telegraph_poster import TelegraphPoster

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

def post_to_telegraph(a_title: str, content: str) -> str:
    """Create a Telegram Post using HTML Content"""
    post_client = TelegraphPoster(use_api=True)
    auth_name = "virusberdana"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=a_title,
        author=auth_name,
        author_url="https://t.me/virusberdana",
        text=content,
    )
    return post_page["url"]