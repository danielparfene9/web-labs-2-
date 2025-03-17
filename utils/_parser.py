from ._utils import HTMLParser, List, BaseModel, Field

class HTMLExtractorConfig(BaseModel):
    convert_charrefs: bool = Field(default=True, description="Convert character references like &amp; to &")


class HTMLExtractor(HTMLParser):
    
    def __init__(self, config: HTMLExtractorConfig = HTMLExtractorConfig()) -> None:
        super().__init__(convert_charrefs=config.convert_charrefs)
        self.text: List[str] = []

    def handle_data(self, data: str) -> None:
        cleaned_text = data.strip()
        if cleaned_text:
            self.text.append(cleaned_text)

    def get_text(self) -> str:
        return " ".join(self.text)

    @classmethod
    def from_html(cls, html: str, config: HTMLExtractorConfig = HTMLExtractorConfig()) -> str:
        parser = cls(config)
        parser.feed(html)
        return parser.get_text()
