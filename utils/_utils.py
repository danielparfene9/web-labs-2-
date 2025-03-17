import os, socket, re
from typing import Dict, Optional, List
from html.parser import HTMLParser
from pydantic import BaseModel, Field

from ._http_request import HTTPClient as Client
from ._parser import HTMLExtractor as Parser
from ._search import SearchEngine as Search

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
    "Field",
    "Client",
    "Parser",
    "Search"
]