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

    @staticmethod
    def _parse_http_response(response: bytes) -> Optional[str]:
        try:
            headers, body = response.split(b"\r\n\r\n", 1)

            html_content = body.decode(errors="ignore")
            return HTMLExtractor.from_html(html_content)
        except ValueError:
            return None