from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import requests
import json
import hashlib

class BBC_NEWS:
	def __init__(self, bbc_url):
		self.url = bbc_url

	def getNewsHeadlines(self):


		bbc_news_headlines = []

		page_response = self.__tryRequestGet(self.url)

		if page_response['status'] == 0:
			
			page_content = BeautifulSoup(page_response["msg"].content, "html.parser")

			site_sections_content = page_content.find("div", class_ = "gel-wrap gs-u-pt+").find_all('a')

			for content in site_sections_content:
				headline = content.find('h3')
				content_url = 'https://www.bbc.com' + content['href']

				# The hashlib md5 hashing function only takes a sequence of bytes as a parameter thus the need to encode the content url
				headline_hash_object = hashlib.md5(content_url.encode())
				headline_id = headline_hash_object.hexdigest()

				if headline is not None:
					data = {
					"title":headline.get_text(),
					"news_url":content_url,
					"news_title_id": headline_id
					}

					bbc_news_headlines.append(data)

				else:
					pass

			data = {
			"status":0,
			"msg": bbc_news_headlines
			}

			print(json.dumps(data, indent=4, sort_keys=True))

		else:
			data = {
			"status": 1,
			"msg": page_response["msg"]
			}

		return data



	def __tryRequestGet(self, url):

		try:
			bbcNews_link_response = requests.get(url, timeout=6)

		except Exception as e:

			data = {
			"status": 1,
			"msg": e
			}

			return data

		data = {
		"status": 0,
		"msg": bbcNews_link_response
		}

		return data





bbc_news_headlines = BBC_NEWS('https://www.bbc.com/news')

bbc_news_headlines.getNewsHeadlines()

# response = requests.get('https://www.bbc.com/news', timeout=6)

# page_content = BeautifulSoup(response.content, "html.parser")

# site_sections_content = page_content.find("div", class_ = "gel-wrap gs-u-pt+").find_all('a')

# articles = []
# for x in site_sections_content:
# 	v = x.find('h3')
# 	content_url = 'https://www.bbc.com' + x["href"]
# 	headline_content = v

# 	if v is not None:
# 		data = {
# 		"title":v.get_text(),
# 		"url":content_url
# 		}

# 		articles.append(data)

# data2 = {
# 	"status":0,
# 	"msg":articles
# }
# print(json.dumps(data2, indent=4, sort_keys=True))

# print(len(articles))


