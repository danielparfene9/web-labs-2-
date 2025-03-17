import os, socket, re
from typing import Dict, Optional, List
from html.parser import HTMLParser
from pydantic import BaseModel, Field

USER_AGENT = "go2web-cli/1.0"
CACHE_DIR = ".go2web_cache"
ENGINE_URL = "http://duckduckgo.com/html?q="

__all__ = [
    "os",
    "socket",
    "re",
    "Dict",
    "Optional",
    "List",
    "HTMLParser",
    "BaseModel",
    "Field"
]