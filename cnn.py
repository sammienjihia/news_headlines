import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import json

class SplashScraper:

    def __init__(self, base_url):

        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme, urlparse(self.base_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.scraped_pages = set([])
        self.to_crawl = Queue()
        self.to_crawl.put(self.base_url)

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        found_urls = []
        for link in links:
            url = link['href']
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scraped_pages:
                    self.to_crawl.put(url)

    def scrape_info(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all('div', {'class': 'product-detail'})
        if products:
            for product in products:
                name = product.find('p', {'class':'margin-bottom-xxl'})
                price = product.find('div', {'class': 'price'})
                if name and price:
                    with open('product-details.csv', 'a') as output:
                        output.write('"{}","{}"\n'.format(name.get_text(), price.get_text()))

    def post_scrape_callback(self, res):
        result = res.result()
        if result.status_code == 200:
            self.parse_links(result.text)
            self.scrape_info(result.text)

    def scrape_page(self, url):
        res = requests.get('{}'.format(url))
        return res

    def run_scraper(self):
        while True:
            try:
                target_url = self.to_crawl.get(timeout=120)
                if target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue

# if __name__ == '__main__':
#     s = SplashScraper("https://edition.cnn.com")
#     s.run_scraper()


from selenium import webdriver
import sys

try:
	driver = webdriver.PhantomJS("/home/sammy/6news/drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
except Exception as e :
	data = {
	"status": 0,
	"msg": str(e) + " Check your webdriver installation"
	}
	print(data)
	sys.exit()
driver.get("https://edition.cnn.com")

html = driver.execute_script("return document.documentElement.outerHTML")

sel_soup = BeautifulSoup(html, 'html.parser')

# print(sel_soup.find('div'), {'id':'intl_homepage1-zone-1'})


p_element = driver.find_element_by_id(id_ = "intl_homepage1-zone-1")



print("***************")

yu = []
for i in sel_soup.find_all("a"):
	#print(i["href"])
	r = {
	"title":i.text,
	"uri":i["href"],
	
	}
	yu.append(r)
	
print("***********************************")


# http://us.cnn.com

base_url = "http://us.cnn.com"
section0 = sel_soup.find("div", {'class':"column zn__column--idx-0"}).find("ul")

trending_news = []

for i in section0.find_all("li"):

	url = base_url + i.find("a")["href"]
	title =  i.find("a").get_text()

	r = {
	"uri": url,
	"title": title
	}

	trending_news.append(r)



section1 = sel_soup.find("div", {'class':"column zn__column--idx-1"}).find("ul")

for i in section1.find_all("li"):

	url = base_url + i.find("a")["href"]
	title =  i.find("a").get_text()

	r = {
	"uri": url,
	"title": title
	}

	trending_news.append(r)



section2 = sel_soup.find("div", {'class':"column zn__column--idx-2"}).find("ul")

for i in section2.find_all("li"):

	url = base_url + i.find("a")["href"]
	title =  i.find("a").get_text()

	r = {
	"uri": url,
	"title": title
	}

	trending_news.append(r)

print(json.dumps(trending_news , indent=4, sort_keys=True))

import re
print("*************")

# print(len(sel_soup.find("div", {'class':"pg-no-rail pg-wrapper"}).find_all("div", {'class': re.compile("^l-container")})))

# for x in (sel_soup.find_all("div", {'class':"zn__containers"})):
# 	print(x.find("ul")["class"])




re.compile("^l-container")



#print(yu)
# for i in sel_soup.find_all("section"):
# 	print(i["class"])

# articleLink_response = requests.get("https://edition.cnn.com", timeout=6)

# articleLink_content = BeautifulSoup(articleLink_response.text, "html.parser")

# cont = articleLink_content.find_all("article")

# for x in cont:
# 	print(x.get_text())





# intl_homepage1-zone-1

# intl_homepage1-zone-2 Doesn't work


"""

[  
   {  
      "id":"intl_homepage1-zone-1"
   },
   {  
      "id":"intl_homepage-magellan-zone-1",
      "uri":"intl_index3.html"
   },
   {  
      "id":"intl_homepage-magellan-zone-2",
      "uri":"intl_index3.html"
   },
   {  
      "id":"intl_homepage-magellan-zone-3",
      "uri":"intl_index3.html"
   },
   {  
      "id":"intl_homepage-magellan-zone-4",
      "uri":"intl_index3.html"
   },
   {  
      "id":"intl_homepage3-zone-4"
   }
]



['HTML_FORMATTERS', 'XML_FORMATTERS', '__bool__', '__call__', '__class__', '__contains__', '__copy__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_all_strings', '_find_all', '_find_one', '_formatter_for_name', '_is_xml', '_lastRecursiveChild', '_last_descendant', '_should_pretty_print', 'append', 'attrs', 'can_be_empty_element', 'childGenerator', 'children', 'clear', 'contents', 'decode', 'decode_contents', 'decompose', 'descendants', 'encode', 'encode_contents', 'extend', 'extract', 'fetchNextSiblings', 'fetchParents', 'fetchPrevious', 'fetchPreviousSiblings', 'find', 'findAll', 'findAllNext', 'findAllPrevious', 'findChild', 'findChildren', 'findNext', 'findNextSibling', 'findNextSiblings', 'findParent', 'findParents', 'findPrevious', 'findPreviousSibling', 'findPreviousSiblings', 'find_all', 'find_all_next', 'find_all_previous', 'find_next', 'find_next_sibling', 'find_next_siblings', 'find_parent', 'find_parents', 'find_previous', 'find_previous_sibling', 'find_previous_siblings', 'format_string', 'get', 'getText', 'get_attribute_list', 'get_text', 'has_attr', 'has_key', 'hidden', 'index', 'insert', 'insert_after', 'insert_before', 'isSelfClosing', 'is_empty_element', 'known_xml', 'name', 'namespace', 'next', 'nextGenerator', 'nextSibling', 'nextSiblingGenerator', 'next_element', 'next_elements', 'next_sibling', 'next_siblings', 'parent', 'parentGenerator', 'parents', 'parserClass', 'parser_class', 'prefix', 'preserve_whitespace_tags', 'prettify', 'previous', 'previousGenerator', 'previousSibling', 'previousSiblingGenerator', 'previous_element', 'previous_elements', 'previous_sibling', 'previous_siblings', 'recursiveChildGenerator', 'renderContents', 'replaceWith', 'replaceWithChildren', 'replace_with', 'replace_with_children', 'select', 'select_one', 'setup', 'string', 'strings', 'stripped_strings', 'text', 'unwrap', 'wrap']


"""

driver2 = webdriver.PhantomJS("/home/sammy/6news/drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
driver2.get("http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html")

# html = driver2.execute_script("return document.documentElement.outerHTML")

html2 = requests.get("http://us.cnn.com/2019/01/28/opinions/theresa-may-brexit-trail-gbr-intl/index.html")

sel_soup = BeautifulSoup(html2.content, 'html.parser')

# sel_soup = BeautifulSoup(html, 'html.parser')

content = sel_soup.find("div", {'class':'pg-rail-tall__body'}).find("div", {'class':'l-container'})


