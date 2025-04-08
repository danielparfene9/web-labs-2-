from ._utils import json, os, time, Optional, Dict

CACHE_FILE = "http_cache.json"

class HTTPCache:
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                self.cache = json.load(f)

    def _save(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)

    def get(self, url: str) -> Optional[Dict]:
        entry = self.cache.get(url)
        if not entry:
            return None
        if time.time() > entry.get("expires", 0):
            return None
        return entry

    def set(self, url: str, status_code: int, headers: Dict[str, str], body: str, ttl: int = 60):
        self.cache[url] = {
            "expires": time.time() + ttl,
            "status_code": status_code,
            "headers": headers,
            "body": body
        }
        self._save()