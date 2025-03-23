import os, socket, re, ssl
from typing import Dict, Optional, List
from html.parser import HTMLParser
from pydantic import BaseModel, Field

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
CACHE_DIR = ".go2web_cache"
ENGINE_URL = "https://www.google.com/search?q="

__all__ = [
    "os",
    "socket",
    "re",
    "Dict",
    "Optional",
    "List",
    "HTMLParser",
    "BaseModel",
    "Field",
    "ssl"
]