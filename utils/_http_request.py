from ._utils import USER_AGENT, Optional, Dict, socket, re, ssl, MAX_REDIRECTS
from ._parser import HTMLExtractor as Parser

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

            html_content = body.decode('utf-8', errors="ignore")
            return Parser.from_html(html_content)
        except ValueError:
            return None
        
    @staticmethod
    def send_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, timeout=10) -> Optional[str]:
        if url.startswith("http://"):
            host, path = url.split("/", 3)[2], "/" + url.split("/", 3)[3] if "/" in url[7:] else "/"
            port = 80
        elif url.startswith("https://"):
            host, path = url.split("/", 3)[2], "/" + url.split("/", 3)[3] if "/" in url[8:] else "/"
            port = 443
        else:
            raise ValueError("Invalid URL scheme. Only HTTP and HTTPS are supported.")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if port == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            sock.sendall(request.encode())
            
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk

        return response
    
    @staticmethod
    def get_response(response):
        return HTTPClient._parse_http_response(response)
    