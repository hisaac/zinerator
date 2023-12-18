import re
import sys
from pathlib import Path

from courlan import clean_url
from HTMLDocument import HTMLDocument
from trafilatura import extract, fetch_url
from weasyprint import HTML

ROOT_DIR = Path(__file__).parent.parent


def main() -> int:
	urls: list[str] = read_url_file()
	cleaned_urls: list[str] = clean_urls(urls)
	fetched_html_documents: list[HTMLDocument] = fetch_urls(cleaned_urls)
	extracted_html_documents: list[HTMLDocument] = extract_url_contents(fetched_html_documents)

	print(extracted_html_documents[0].contents)

	for index, document in enumerate(extracted_html_documents):
		html = HTML(string=document.contents)
		html.write_pdf(
			target=f"{ROOT_DIR}/{index}.pdf",
			zoom=2
		)

	return 0


def read_url_file() -> list[str]:
	with open(ROOT_DIR / "urls.txt", "r") as f:
		return f.readlines()


def clean_urls(urls: list[str]) -> list[str]:
	return [clean_url(url) for url in urls]


def fetch_urls(urls: list[str]) -> list[HTMLDocument]:
	return [HTMLDocument(url, fetch_url(url)) for url in urls]


def extract_url_contents(fetched_urls: list[HTMLDocument]) -> list[HTMLDocument]:
	extracted_urls: list[HTMLDocument] = []

	for url in fetched_urls:
		cleaned_contents = remove_emojis(url.contents)
		extracted = extract(
			cleaned_contents,
			output_format="xmltei",
			url=url.url,
			include_formatting=True,
			include_images=True,
			include_tables=True,
		)
		extracted_urls.append(HTMLDocument(url.url, extracted))

	return extracted_urls


# This is a temporary workaround until lxml is updated
# or trafilatura uses an updated lxml that fixes this issue
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
