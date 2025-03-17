import socket
import re
from typing import Optional, Dict
from ._parser import HTMLExtractor
from ._utils import USER_AGENT

class HTTPClient:

    DEFAULT_HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html",
        "Connection": "close",
    }