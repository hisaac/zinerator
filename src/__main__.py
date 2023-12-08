import sys
from pathlib import Path
import re

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
		cleaned_contents = remove_emojis(url.contents)
		extracted = extract(
			cleaned_contents,
			output_format="xml",
			url=url.url,
			include_formatting=True,
			include_images=True,
			include_tables=True,
		)
		extracted_urls.append(ExtractedURL(url.url, extracted))

	return extracted_urls


# This is a temporary workaround until lxml is updated / trafilatura uses an updated lxml that fixes this issue
def remove_emojis(text):
	emoji_pattern = re.compile(
		"["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		u"\U00002500-\U00002BEF"  # chinese char
		u"\U00002702-\U000027B0"
		u"\U00002702-\U000027B0"
		u"\U000024C2-\U0001F251"
		u"\U0001f926-\U0001f937"
		u"\U00010000-\U0010ffff"
		u"\u2640-\u2642"
		u"\u2600-\u2B55"
		u"\u200d"
		u"\u23cf"
		u"\u23e9"
		u"\u231a"
		u"\ufe0f"  # dingbats
		u"\u3030"
		"]+",
		flags=re.UNICODE
	)
	return emoji_pattern.sub(r'', text)


if __name__ == "__main__":
	sys.exit(main())
