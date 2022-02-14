import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time

word = "blue"
url = "https://giphy.com/search/{}".format(word)

print(url)
data = requests.get(url)

# driver = webdriver.Chrome()
# driver.get (url)

soup = BeautifulSoup(data.text, "lxml")
f = open('black.html', 'w')
f.write(soup.text)
script = soup.find_all("script")[13].text

d = json.loads((script.split(start))[1].split(end)[0])
url = d[0]['images']['source']['url']
left, bracket, rest = url.partition("//")
block, bracket, right = rest.partition(".")
new_url = left + "//" + "i" + "." + right
