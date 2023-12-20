import pathlib
import sys

from .Article import Article
from .parser import parse_article

ROOT_DIR = pathlib.Path(__file__).parent.parent


def main() -> int:
	with open(ROOT_DIR / "urls.txt", "r") as file:
		urls = file.readlines()

	articles: list[Article] = []
	for url in urls:
		article = parse_article(url)
		articles.append(article)
		print("\n---")
		print("URL:", article.url)
		print("Title:", article.title)
		print("Authors:", article.authors)
		print("Publish Date:", article.publish_date)
	# print("Content:", article.content)

	return 0


if __name__ == "__main__":
	sys.exit(main())
