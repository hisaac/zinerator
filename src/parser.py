import json
from subprocess import PIPE, Popen

import requests

from .Article import Article


def parse_article(url: str) -> Article:
	html = get_html(url)

	parsed_content = parse_content(url)

	if parsed_content["title"] is None:
		parsed_content["title"] = parse_title(html)

	if parsed_content["author"] is None:
		parsed_content["author"] = parse_authors(html)

	if parsed_content["date_published"] is None:
		parsed_content["date_published"] = parse_publish_date(html)

	return Article(
		url=url,
		html=html,
		content=parsed_content["content"],
		title=parsed_content["title"],
		authors=parsed_content["author"],
		publish_date=parsed_content["date_published"],
	)


def get_html(url: str) -> str:
	return requests.get(url).content.decode("utf-8")


def parse_content(url: str) -> any:
	process = Popen([
		"npx", "postlight-parser", url,
	], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()

	# TODO: Handle Error
	if process.returncode != 0:
		print(stderr)

	return json.loads(stdout)


def parse_title(html: str) -> str | None:
	return None


def parse_authors(html: str) -> list[str] | None:
	return None


def parse_publish_date(html: str) -> str | None:
	return None
