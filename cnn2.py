import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from selenium import webdriver
import json
import urllib.request


# driver2 = webdriver.PhantomJS("/home/sammy/6news/drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
# driver2.get("http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html")

# # html = driver2.execute_script("return document.documentElement.outerHTML")

# html2 = requests.get("http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html")

# sel_soup = BeautifulSoup(html2.content, 'html.parser')

# # sel_soup = BeautifulSoup(html, 'html.parser')

# content = sel_soup.find("div", {'class':'pg-rail-tall__body'}).find("div", {'class':'l-container'})







# import urllib.request

# import urllib.request
# with urllib.request.urlopen("http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html") as url:
#     html = url.read()


# # url = "http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html"
# # html = urllib.urlopen(url).read()
# soup = BeautifulSoup(html, 'html.parser')

# soup = soup.find("div", {'class':'pg-rail-tall__body'}).find("div", {'class':'l-container'})

# # kill all script and style elements
# for script in soup(["script", "style"]):
#     script.decompose()    # rip it out

# # get text
# text = soup.get_text()

# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)

# # print(text)




class CNN_NEWS:

	def __init__(self, base_url):

		self.base_url = base_url

	def getCNN_NewsContent(self):

		news_content = []

		NewsHeadLines = self.getCNN_NewsHeadlines()

		if NewsHeadLines["status"] == 0:
			list_HeadLines = NewsHeadLines["msg"]

			for headLine in list_HeadLines:

				uri = headLine["uri"]

				try:
					with urllib.request.urlopen(uri) as url:
						html = url.read()

					soup = BeautifulSoup(html, 'html.parser')

					soup = soup.find("div", {'class':'pg-rail-tall__body'}).find("div", {'class':'l-container'})

					# ************* Create a seperate for the article title. We ascend the html tree

					soup2 = BeautifulSoup(html, 'html.parser')

					# Get article title
					title = soup2.find("title").get_text()

					# Get article author and date published or updated
					author_time = soup2.find("div", {'class':'metadata__info js-byline-images'})

					# Get author name
					author = author_time.find("p", {'class':'metadata__byline'}).get_text()

					# Get datetime published
					time = author_time.find("p", {'class':'update-time'}).get_text()

					for script_style in soup(["script", "style"]):
						script_style.decompose() # rip it out
						
					# get text
					text = soup.get_text()

					# break into lines and remove leading and trailing space on each
					lines = (line.strip() for line in text.splitlines())
					# break multi-headlines into a line each
					chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
					# drop blank lines
					text = '\n'.join(chunk for chunk in chunks if chunk)

				except Exception as e:
					text = None
					title = None
					author = None
					time = None
					pass	

				r = {
				"article_content":text,
				"article_title":title,
				"article_author": author,
				"article_PubDate": time
				}

				news_content.append(r)

		else:

			data = {
			"status": 1,
			"msg": "Could Not get CNN news headlines"
			}

		
		data = {
		"status": 0,
		"msg": news_content
		}

		data = json.dumps(data, indent=4, sort_keys=True)

		return data 


	def getCNN_NewsHeadlines(self):

		headlines = []

		"""
		So, CNN's trending news on their website are in 3 sections. 
		section 0 , section 1 and section 2

		"""

		# When deploying to a server, ensure to test for the webdriver and use a different webdriver from this one
		try:
			driver = webdriver.PhantomJS("/home/sammy/6news/drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
		except Exception as e:

			data = {
			"status": 1,
			"msg": str(e) + " Check your web driver installation path!"
			}

			return data


		try:
			driver.get(self.base_url)

		except Exception as e:

			data = {
			"status": 1,
			"msg": str(e)
			}

			return data



		# CNN is a javascript heavy website, so we use the power of the selenium webdriver to extract javascript loaded 
		# contents
		html = driver.execute_script("return document.documentElement.outerHTML")

		sel_soup = BeautifulSoup(html, 'html.parser')

		# Get the news items in section0
		section0 = sel_soup.find("div", {'class':"column zn__column--idx-0"}).find("ul")

		for news_item in section0.find_all("li"):

			news_uri = self.base_url + news_item.find("a")["href"]

			r = {
			"uri": news_uri
			}

			headlines.append(r)

		# Get the news items in section1
		section1 = sel_soup.find("div", {'class':"column zn__column--idx-1"}).find("ul")

		for news_item in section1.find_all("li"):

			news_uri = self.base_url + news_item.find("a")["href"]

			r = {
			"uri": news_uri
			}

			headlines.append(r)

		# Get the news item in section2

		section2 = sel_soup.find("div", {'class':"column zn__column--idx-2"}).find("ul")

		for news_item in section2.find_all("li"):

			news_uri = self.base_url + news_item.find("a")["href"]

			r = {
			"uri": news_uri
			}

			headlines.append(r)


		data = {
		"status":0,
		"msg": headlines
		}

		print(json.dumps(data, indent=4, sort_keys=True))
		print(len(headlines))

		return data


cnn = CNN_NEWS("https://edition.cnn.com")

cnn.getCNN_NewsHeadlines()

print(cnn.getCNN_NewsContent())   # this function is just too slow, kindly refactor




# with urllib.request.urlopen("http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html") as url:
#     html = url.read()



# # soup = BeautifulSoup(html, 'html.parser')

# soup2 = BeautifulSoup(html, 'html.parser')

# # soup = soup.find("div", {'class':'pg-rail-tall__body'}).find("div", {'class':'l-container'})

# title = soup2.find("title").get_text()

# author_time = soup2.find("div", {'class':'metadata__info js-byline-images'})
# author = author_time.find("p", {'class':'metadata__byline'}).get_text()

# time = author_time.find("p", {'class':'update-time'}).get_text()


# print(title)

# print(author)

# print(time)

