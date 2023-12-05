import sys
from pathlib import Path

from courlan import clean_url
from trafilatura import fetch_url, extract

ROOT_DIR = Path(__file__).parent.parent


class FetchedURL:
	url: str
	contents: str | None

	def __init__(self, url: str, contents: str | None) -> None:
		self.url = url
		self.contents = contents

	def __str__(self) -> str:
		return f"URL: {self.url}\nContents: {self.contents}\n"


class ExtractedURL:
	url: str
	contents: str | None

	def __init__(self, url: str, contents: str | None) -> None:
		self.url = url
		self.contents = contents

	def __str__(self) -> str:
		return f"URL: {self.url}\nContents: {self.contents}\n"


def main() -> int:
	urls: list[str] = read_url_file()
	cleaned_urls: list[str] = clean_urls(urls)
	fetched_urls: list[FetchedURL] = fetch_urls(cleaned_urls)
	extracted_urls: list[ExtractedURL] = extract_url_contents(fetched_urls)

	for url in extracted_urls:
		print(url.url)
		print(url.contents)

	return 0


def read_url_file() -> list[str]:
	with open(ROOT_DIR / "urls.txt", "r") as f:
		return f.readlines()


def clean_urls(urls: list[str]) -> list[str]:
	return [clean_url(url) for url in urls]


def fetch_urls(urls: list[str]) -> list[FetchedURL]:
	return [FetchedURL(url, fetch_url(url)) for url in urls]


def extract_url_contents(fetched_urls: list[FetchedURL]) -> list[ExtractedURL]:
	extracted_urls: list[ExtractedURL] = []

	for url in fetched_urls:
		extracted = extract(
			url.contents,
			output_format="xml",
			url=url.url,
			include_formatting=True,
			include_images=True,
			include_tables=True,
		)
		url.contents = extracted
		extracted_urls.append(ExtractedURL(url.url, extracted))

	return extracted_urls


if __name__ == "__main__":
	sys.exit(main())
