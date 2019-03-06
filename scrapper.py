from bs4 import BeautifulSoup
import requests

page_link = "https://www.pulse.ng/bi/lifestyle/flights-halted-at-major-airports-in-new-york-and-philadelphia-as-the-longest/gq45hjt"

page_response = requests.get(page_link, timeout=5)

page_content = BeautifulSoup(page_response.content, "html.parser")

title = page_content.find("title").get_text()

author = page_content.find("span", class_ = 'authorItemName').get_text()

print(title)

print(author)

content = page_content.find_all("div", class_ = 'detail intext articleBody')

datePublished = page_content.find("time", class_ = "datePublished").get_text()

print(datePublished)

content_text = ""
content_text2 = []
for p in content:
	#print(p.get_text())
	content_text += (str(p.get_text()))
	content_text2.append(p.get_text())

print(str(content_text))

print("".join(str(x) for x in content_text2))




