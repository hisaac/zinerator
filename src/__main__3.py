import sys
from pathlib import Path

import newspaper
import pyemoji

ROOT_DIR = Path(__file__).parent.parent


def main() -> int:
	urls: list[str] = read_url_file()
	for url in urls:
		article = newspaper.article(url)

		if not article.is_parsed:
			# newspaper4k doesn't like emojis
			cleaned_html = pyemoji.replace(article.html)
			article.download(input_html=cleaned_html)
			article.parse()

		article.nlp()

		print("Authors", article.authors)
		print("Title", article.title)

	return 0


def read_url_file() -> list[str]:
	with open(ROOT_DIR / "urls.txt", "r") as file:
		return file.readlines()


if __name__ == "__main__":
	sys.exit(main())
