import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from repositories.url_repository import UrlRepository

API_URL = "https://tinyurl.com/api-create.php?url={url}"


class UrlService:
    def __init__(self, repo: UrlRepository | None = None) -> None:
        self.repo = repo or UrlRepository()

    def list_history(self) -> list[dict]:
        return self.repo.load()

    def get_by_id(self, entry_id: int) -> dict | None:
        return next((e for e in self.repo.load() if e["id"] == entry_id), None)

    def shorten(self, long_url: str) -> tuple[dict | None, str | None]:
        long_url = long_url.strip()
        if not long_url:
            return None, "URL cannot be empty."
        if not long_url.startswith(("http://", "https://")):
            long_url = "https://" + long_url
        try:
            short_url = self._call_api(long_url)
        except (ConnectionError, ValueError) as e:
            return None, str(e)
        history = self.repo.load()
        entry = {
            "id": (max((e["id"] for e in history), default=0) + 1),
            "original_url": long_url,
            "short_url": short_url,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.repo.add(entry)
        return entry, None

    @staticmethod
    def _call_api(long_url: str) -> str:
        api_request = API_URL.format(url=urllib.parse.quote(long_url, safe=""))
        try:
            with urllib.request.urlopen(api_request, timeout=15) as response:
                short_url = response.read().decode("utf-8").strip()
        except urllib.error.URLError as e:
            raise ConnectionError(f"API request failed: {e}") from e
        if not short_url.startswith("http"):
            raise ValueError(f"Invalid response from API: {short_url}")
        return short_url
