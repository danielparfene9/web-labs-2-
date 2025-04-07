from ._utils import USER_AGENT, Optional, Dict, socket, re, ssl, MAX_REDIRECTS, Tuple, HTTPResponse
from ._parser import HTMLExtractor as Parser

class HTTPClient:

    DEFAULT_HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html",
        "Connection": "close",
    }

    @staticmethod
    def _parse_http_response(response: bytes) -> Tuple[int, Dict[str, str], Optional[str]]:
        try:
            headers, body = response.split(b"\r\n\r\n", 1)

            header_lines = headers.decode('utf-8', errors='ignore').split("\r\n")
            status_line = header_lines[0]

            try:
                status_code = int(status_line.split(" ")[1])
            except (IndexError, ValueError):
                status_code = 0

            headers_kv = {}
            for line in header_lines[1:]:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    headers_kv[key.strip()] = value.strip()

            html_content = body.decode('utf-8', errors="ignore")
            parsed_html = Parser.from_html(html_content)

            return status_code, headers_kv, parsed_html
        except ValueError:
            return 0, {}, None
        
    @staticmethod
    def send_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, timeout=10, redirect_remaining = 5) -> Optional[str]:
        
        if redirect_remaining <= 0:
            raise Exception("Too many redirects")
        
        if url.startswith("http://"):
            scheme = "http"
            host, path = url.split("/", 3)[2], "/" + url.split("/", 3)[3] if "/" in url[7:] else "/"
            port = 80
        elif url.startswith("https://"):
            scheme = "https"
            host, path = url.split("/", 3)[2], "/" + url.split("/", 3)[3] if "/" in url[8:] else "/"
            port = 443
        else:
            raise ValueError("Invalid URL scheme. Only HTTP and HTTPS are supported.")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if port == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.settimeout(timeout)
            sock.connect((host, port))

            req_headers = headers or HTTPClient.DEFAULT_HEADERS
            header_lines = "\r\n".join([f"{k}: {v}" for k, v in req_headers.items()])
            request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n{header_lines}\r\n\r\n"
            sock.sendall(request.encode())
            
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk

        status_code, response_headers, _ = HTTPClient._parse_http_response(response)
        if status_code in (301, 302, 307, 308):
            location = response_headers.get("Location")
            if not location:
                raise Exception("Redirect status but no Location header found")
            if location.startswith("/"):
                location = f"{scheme}://{host}{location}"
            return HTTPClient.send_request(location, method, headers, timeout, redirect_remaining - 1)
        
        return response
    
    @staticmethod
    def get_response(response: bytes) -> HTTPResponse:
        status_code, headers, body = HTTPClient._parse_http_response(response)
        return HTTPResponse(status_code=status_code, headers=headers, body=body)

    