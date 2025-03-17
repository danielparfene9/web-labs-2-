from ._utils import USER_AGENT, Optional, Dict, socket, re, Parser

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
            return Parser.from_html(html_content)
        except ValueError:
            return None
        
    @staticmethod
    def send_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None) -> Optional[str]:
        parsed = re.match(r"https?://([^/]+)(.*)", url)
        if not parsed:
            return None

        host, path = parsed.groups()
        path = path or "/"
        port = 80

        request_headers = {**HTTPClient.DEFAULT_HEADERS, **(headers or {})}

        request_lines = [
            f"{method} {path} HTTP/1.1",
            f"Host: {host}",
            *[f"{key}: {value}" for key, value in request_headers.items()],
            "",
        ]

        request = "\r\n".join(request_lines)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # IPv4 + TCP
                sock.connect((host, port))
                sock.sendall(request.encode())

                response = b""
                while chunk := sock.recv(4096):
                    response += chunk
        except (socket.error, ConnectionError) as e:
            return None

        return HTTPClient._parse_http_response(response)
    