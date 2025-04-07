from ._utils import ENGINE_URL, re, List, Tuple, BeautifulSoup
from ._http_request import HTTPClient as Client
from urllib.parse import urlparse, parse_qs, unquote

class SearchError(Exception):
    pass

class SearchEngine:

    @staticmethod
    def search_term(term: str) -> str:
        search_url = f"{ENGINE_URL}{'+'.join(term.split())}"

        response = Client.send_request(search_url)
        if not response:
            raise SearchError("Failed to fetch search results.")

        # readable_text = Client._parse_http_response(response)
        # if not readable_text:
        #     raise SearchError("Could not extract text from the response.")

        results = SearchEngine._extract_links(response)

        if not results:
            raise SearchError("No search results found.")

        return SearchEngine._format_results(results)

    @staticmethod
    def _extract_links(html_content: str) -> List[Tuple[str, str]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        for a_tag in soup.find_all('a', href=True):
            raw_href = a_tag['href']
            title = a_tag.get_text(strip=True)

            if not title:
                continue

            if "duckduckgo.com/l/?" in raw_href and "uddg=" in raw_href:
                parsed_url = urlparse(raw_href)
                query_params = parse_qs(parsed_url.query)
                actual_url = unquote(query_params.get("uddg", [""])[0])
                if actual_url.startswith("http"):
                    results.append((actual_url, title))

            elif raw_href.startswith("http"):
                results.append((raw_href, title))

        return results

    @staticmethod
    def _format_results(results: List[tuple]) -> str:
        return "\n".join([f"{i+1}. {title} - {link}" for i, (link, title) in enumerate(results[:10])])
