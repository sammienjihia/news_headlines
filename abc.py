from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import requests
import json

class ABC_NEWS:
	def __init__(self, abc_url):
		self.url = abc_url

	def getNewsHeadlines(self):

		page_link = self.url

		abc_news_links = []

		page_response = self.__tryRequestGet(page_link)

		if page_response["status"] == 0 :



			page_content = BeautifulSoup(page_response["msg"].content, "html.parser")

			site_headline_links = page_content.find("ul", class_ = "headlines-ul").find_all("li")

			for link in site_headline_links:

				sm = link.find("a")

				data = {
				"title":sm.get_text(),
				"news_url":sm["href"],
				"news_title_id":link["data-id"]
				}


				# removing leading and trailing '/'
				url_path = str(urlparse(data["news_url"]).path).strip('/')
				urls_tags = url_path.split('/')
				data["tags"] = urls_tags[0].lower()

				data1 = json.dumps(data)

				abc_news_linksJson = json.loads(data1)
				abc_news_links.append(abc_news_linksJson)

			data = {
			"status":0,
			"msg": abc_news_links
			}

		else:
			data = {
			"status": 1,
			"msg": page_response["msg"]
			}

		return data

	def getNewsContent(self):

		newsHeadlines = self.getNewsHeadlines()

		if newsHeadlines["status"] == 0 :
			# do something

			content_list = []

			for article in newsHeadlines["msg"]:

				article_url = article['news_url']
				article_tag = article['tags']
				article_id = article["news_title_id"]



				try:


					some_Content = self.__getContent(article_url)

					if some_Content["status"] == 0 :


						r = {
						"article_url":article_url,
						"article_tag":article_tag,
						"article_id": article_id,
						"article_content": some_Content["msg"]
						}
						content_list.append(r)

					else:
						pass

				except Exception as e :
					pass





			data = {
			"status":0,
			"msg": content_list
			}


		else:
			data = {
			"status" : 1,
			"msg" : "News contents could not be found"
			}

		# print(json.dumps(data, indent=4, sort_keys=True))

		data = json.dumps(data, indent=4, sort_keys=True)

		return data


	def __tryRequestGet(self, url):

		try:

			articleLink_response = requests.get(url, timeout=6)



		except requests.exceptions.Timeout as e :
			data = {
			"status": 1,
			"msg": e
			}

			return data
		except requests.exceptions.TooManyRedirects as e:
			data = {
			"status": 1,
			"msg": e
			}

			return data

		except requests.exceptions.RequestException as e:
			data = {
			"status": 1,
			"msg": e
			}

			return data

		data = {
		"status": 0,
		"msg": articleLink_response
		}

		return data


	def __getContent(self, article_url):

		articleLink_response = self.__tryRequestGet(article_url)

		if articleLink_response["status"] == 0:

			articleLink_content = BeautifulSoup(articleLink_response["msg"].content, "html.parser")

			try:
				article_image_url = articleLink_content.find("img")["src"]
			except Exception as e :
				article_image_url = None
				pass


			try:
				author = articleLink_content.find("div", class_ = "author").get_text().strip()

			except:
				author = None
				pass


			try:
				date_published = articleLink_content.find("span", class_ = "timestamp").get_text().replace(",", "")[-23:-2]
			except:
				date_published = None
				pass

			news_Content = articleLink_content.find_all("p", itemprop="articleBody")

			content_text = ""

			for text in news_Content:
				x = text.get_text().encode('ascii', 'ignore')
				x = x.decode('utf8')
				content_text += x.strip()

			print(type(content_text))

			print(str(content_text))


			data = {
			"status": 0,
			"msg":{"author":author, "datePublished":date_published, "newsContentText": content_text, "articleImg_url":article_image_url }
			}

		else:
			data = {
			"status": 1,
			"msg": articleLink_response["msg"]
			}

		return data


		



abc = ABC_NEWS("https://abcnews.go.com/")

print(json.dumps(abc.getNewsHeadlines() , indent=4, sort_keys=True))


# print(abc.getNewsContent())

