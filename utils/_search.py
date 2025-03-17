from ._utils import Client, ENGINE_URL, re, List, Optional

def search_term(term):
    search_url = ENGINE_URL + "+".join(term.split())
    response = Client.send_request(search_url)
    readable_text = Client._parse_http_response(response)

    results = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', readable_text)
    if not results:
        return "No search results found."

    output = "\n".join([f"{i+1}. {title} - {link}" for i, (link, title) in enumerate(results[:10])])
    return output
