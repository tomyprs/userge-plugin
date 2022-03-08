""" this thing will be used as plugin doc string """

# here you can do initializing things or keep shared data which will be used by other plugins

# for example

import os
from .aiohttp_helper import AioHttp as get_response

# this is a constant (not going to change)
API_KEY = os.getenv("API_KEY")

# these values can be changed in runtime
class Dynamic:
    TIMEOUT = 60


def shared_method() -> None:
    pass

