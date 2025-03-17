from ._utils import ENGINE_URL, re, List
from ._http_request import HTTPClient as Client

class SearchError(Exception):
    pass

class SearchEngine:

    @staticmethod
    def search_term(term: str) -> str:
        search_url = f"{ENGINE_URL}{'+'.join(term.split())}"

        response = Client.send_request(search_url)
        if not response:
            raise SearchError("Failed to fetch search results.")

        readable_text = Client._parse_http_response(response)
        if not readable_text:
            raise SearchError("Could not extract text from the response.")

        results = SearchEngine._extract_links(readable_text)
        if not results:
            raise SearchError("No search results found.")

        return SearchEngine._format_results(results)

    @staticmethod
    def _extract_links(html_content: str) -> List[tuple]:
        return re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', html_content)

    @staticmethod
    def _format_results(results: List[tuple]) -> str:
        return "\n".join([f"{i+1}. {title} - {link}" for i, (link, title) in enumerate(results[:10])])
