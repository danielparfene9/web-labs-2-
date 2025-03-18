from ._utils import USER_AGENT, Optional, Dict, socket, re, ssl
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

            html_content = body.decode(errors="ignore")
            return Parser.from_html(html_content)
        except ValueError:
            return None
        
    @staticmethod
    def send_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, timeout=10) -> Optional[str]:
        parsed = re.match(r"https?://([^/]+)(.*)", url)
        if not parsed:
            return None

        host, path = parsed.groups()
        path = path or "/"
        is_https = url.startswith("https://")
        port = 80 if not is_https else 443
        request_headers = {**HTTPClient.DEFAULT_HEADERS, **(headers or {})}

        request_lines = [
            f"{method} {path} HTTP/1.1",
            f"Host: {host}",
            *[f"{key}: {value}" for key, value in request_headers.items()],
            "",
        ]

        request = "\r\n".join(request_lines)
        print(f"\n[DEBUG] Connecting to: {host} on port {port}")

        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                print("[DEBUG] Connection successful")
                if is_https:
                    print("[DEBUG] Wrapping socket in SSL")
                    context = ssl.create_default_context()
                    context.minimum_version = ssl.TLSVersion.TLSv1_2
                    sock = context.wrap_socket(sock, server_hostname=host)

                print("[DEBUG] Sending request:")
                print(request)
                sock.sendall(request.encode())

                response = b""
                while chunk := sock.recv(4096):
                    response += chunk

                print("[DEBUG] Received response")
        except socket.timeout:
            print("Request timed out.")
            return None
        except (socket.error, ssl.SSLError) as e:
            print("Can't connect: {e}")
            return None

        return HTTPClient._parse_http_response(response)
    