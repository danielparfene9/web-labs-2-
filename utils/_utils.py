import os, socket, re, ssl, json, time
from typing import Dict, Optional, List, Tuple
from html.parser import HTMLParser
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from dataclasses import dataclass

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
CACHE_DIR = ".go2web_cache"
ENGINE_URL = "https://html.duckduckgo.com/html/?q="
MAX_REDIRECTS = 5

@dataclass
class HTTPResponse:
    status_code: int
    headers: Dict[str, str]
    body: Optional[str]

    def __str__(self):
        lines = [
            f"Status Code: {self.status_code}",
            "Headers:",
            *[f"  {k}: {v}" for k, v in self.headers.items()],
            "",
            "Body (first 500 chars):",
            self.body[:500] + "..." if self.body else "[No body]"
        ]
        return "\n".join(lines)

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
    "ssl",
    "Tuple",
    "BeautifulSoup",
    "json",
    "time"
]