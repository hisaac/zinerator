class HTMLDocument:
	url: str
	contents: str | None

	def __init__(self, url: str, contents: str | None) -> None:
		self.url = url
		self.contents = contents

	def __str__(self) -> str:
		return f"URL: {self.url}\nContents: {self.contents}\n"
