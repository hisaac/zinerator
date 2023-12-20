import json
import sys
from pathlib import Path
from subprocess import PIPE, Popen

from bs4 import BeautifulSoup, HTMLFormatter
from slugify import slugify

ROOT_DIR = Path(__file__).parent.parent


def main() -> int:
	with open(ROOT_DIR / "urls.txt", "r") as file:
		urls: list[str] = file.readlines()

	for url in urls:
		process = Popen([
			"npx", "postlight-parser", url,
		], stdout=PIPE, stderr=PIPE)
		stdout, stderr = process.communicate()

		if process.returncode != 0:
			print(stderr)
			return process.returncode

		data = json.loads(stdout)
		soup = BeautifulSoup(data["content"], "html5lib")

		title_tag = soup.new_tag("title")
		title_tag.string = data["title"]
		soup.head.append(title_tag)

		# What can I say, I like tabs…
		formatter = HTMLFormatter()
		formatter.indent = "	"
		pretty_soup = soup.prettify(formatter=formatter)

		slugified_title = slugify(data["title"])
		with open(f"{ROOT_DIR}/export-{slugified_title}.html", "w") as file:
			file.write(pretty_soup)

	return 0


if __name__ == "__main__":
	sys.exit(main())
