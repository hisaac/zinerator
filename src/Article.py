from dataclasses import dataclass


@dataclass
class Article:
	url: str
	html: str

	content: str | None = None

	title: str | None = None
	authors: list[str] | None = None
	publish_date: str | None = None
