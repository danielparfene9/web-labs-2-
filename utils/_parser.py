from ._utils import HTMLParser, List, BaseModel, Field, json

class HTMLExtractorConfig(BaseModel):
    convert_charrefs: bool = Field(default=True, description="Convert character references like &amp; to &")


class HTMLExtractor(HTMLParser):
    
    def __init__(self, config: HTMLExtractorConfig = HTMLExtractorConfig()) -> None:
        super().__init__(convert_charrefs=config.convert_charrefs)
        self.text: List[str] = []
        self._inside_ignored_tag = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self._inside_ignored_tag = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._inside_ignored_tag = False

    def handle_data(self, data: str) -> None:
        if self._inside_ignored_tag:
            return
        cleaned_text = data.strip()
        if cleaned_text:
            self.text.append(cleaned_text)

    def get_text(self) -> str:
        return " ".join(self.text)

    @classmethod
    def from_html(cls, content: str, config: HTMLExtractorConfig = HTMLExtractorConfig()) -> str:
        content = content.strip()

        if (content.startswith("{") and content.endswith("}")) or \
           (content.startswith("[") and content.endswith("]")):
            try:
                json_obj = json.loads(content)
                return cls._extract_text_from_json(json_obj)
            except json.JSONDecodeError:
                pass

        parser = cls(config)
        parser.feed(content)
        return parser.get_text()

    @staticmethod
    def _extract_text_from_json(obj) -> str:

        text_chunks = []

        def recurse(value):
            if isinstance(value, dict):
                for v in value.values():
                    recurse(v)
            elif isinstance(value, list):
                for item in value:
                    recurse(item)
            elif isinstance(value, str):
                clean = value.strip()
                if clean:
                    text_chunks.append(clean)

        recurse(obj)
        return " ".join(text_chunks)
