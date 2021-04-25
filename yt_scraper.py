import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint
from selenium.webdriver import Chrome
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.chrome.options import Options  
import csv

available = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

def isLink(tag):
	try:
		if tag['href'] != None:
			return True 
	except:
		return False

def isYoutubeLink(link):
	try:
		if link[7:36] == 'https://www.youtube.com/watch':
			return True
		return False
	except:
		return False
linksList = []
def creatValidLinks(string):
	ans = string[7:36] + '?v='
	for i in range(43,len(string)):
		if string[i] == '&':
			break 
		else:
			ans  = ans + string[i]

	return ans

def cleanText(text):
	cleanedText = ''
	for item in text:
		if item in available:
			cleanedText = cleanedText + item 
		else:
			cleanedText = cleanedText + ' '
	return cleanedText


def creatList():
	print("Enter the topic")
	topic = input()
	keyword = [w for w in topic.split(' ')]
	var_req = ''
	url1 = "https://www.google.com/search?q="
	for item in keyword:
		var_req = var_req + ' ' + item
	var_req = var_req + 'youtube'
	url2 = "&source=lnms&tbm=vid"
	url = url1 + var_req + url2                                                                                                                     
	request_result=requests.get( url )
	  
	soup = BeautifulSoup(request_result.text,"lxml")
	videoObj = soup.findAll(isLink)
	arr = []
	for l in videoObj:
		allLink = str(l["href"])
		if isYoutubeLink(allLink):
			arr.append(str(l["href"]))
		else:
			pass
	for link in arr:
		validLink = creatValidLinks(link)
		linksList.append(validLink)
	finalList = list()
	for link in linksList:
		if link in finalList:
			pass
		else:
			finalList.append(link)
	print("Enter number of google pages to scrap after the first page:")
	req = int(input())

	
	option = webdriver.ChromeOptions()
	option.add_argument('headless')
	driver1 = Chrome(options=option)
	driver1.implicitly_wait(5)
	driver1.get(url)
	time.sleep(5)
	newlinks  = driver1.find_elements_by_class_name("fl")
	print(len(newlinks))
	for item in newlinks[1:req + 1]:
		url = item.get_attribute("href")
		request_result=requests.get(str(url))
	  
		soup = BeautifulSoup(request_result.text,"lxml")
		videoObj = soup.findAll(isLink)
		for l in videoObj:
			allLink = str(l["href"])
			if isYoutubeLink(allLink):
				arr.append(str(l["href"]))
			else:
				pass
		for link in arr:
			validLink = creatValidLinks(link)
			linksList.append(validLink)
		finalList = list()
		for link in linksList:
			if link in finalList:
				pass
			else:
				finalList.append(link)



	return finalList

finalList = creatList()
pprint(finalList)


from collections import defaultdict
completeInfo  = defaultdict(dict)

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = Chrome(options=option)
driver.implicitly_wait(5)
digits = '1234567890'
for url in finalList:
	driver.get(url)
	time.sleep(5)
	video_title_list = driver.find_elements_by_class_name("title.style-scope.ytd-video-primary-info-renderer")
	title = cleanText(str(video_title_list[0].text))
	like_dislike_list = driver.find_elements_by_class_name("style-scope.ytd-toggle-button-renderer.style-text")
	count = 0 
	for item in like_dislike_list:
		completeInfo[title]['like'] = 0
		completeInfo[title]['dislike'] = 0
		if item.get_attribute("aria-label") != None:
			if count == 0:
				var1 = str(item.get_attribute("aria-label"))
				f_var1 = ''
				for num in var1:
					if num in digits:
						f_var1 = f_var1 + num 
				if len(f_var1) == 0:
					f_var1 = '0'
				completeInfo[title]['like'] = int(f_var1)
				count = count + 1 
			elif count == 1:
				var1 = str(item.get_attribute("aria-label"))
				f_var1 = ''
				for num in var1:
					if num in digits:
						f_var1 = f_var1 + num 
				if len(f_var1) == 0:
					f_var1 = '0'

				completeInfo[title]['dislike'] = int(f_var1)
		else:
			pass
	chanel_name_list = driver.find_elements_by_class_name("yt-simple-endpoint.style-scope.yt-formatted-string")
	for item in chanel_name_list:
		if item.text!='':
			if item.text[0] != '#':
				completeInfo[title]["channel Name"] = cleanText(str(item.text))
				#pprint(item.get_attribute("aria-label"))
				break
	
	completeInfo[title]['url'] = url 



info = []
for k,v in completeInfo.items():
	temp = [k]
	for val in v.values():
		temp.append(val)
	info.append(temp)

pprint(info)

info = [["Title","Likes","dislikes","Channel","Url"]] + info

with open("newFile.csv", "w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(info)





"""
for link in finalList[0:1]:
		url = link                                                                                                                   
		request_result2=requests.get(url)
		soup2 = BeautifulSoup(request_result2.text,"lxml")
		obj2 =soup2.find_all(   )
		print(obj2[0])
		<a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UC4JX40jDee_tINbkjycV4Sg" dir="auto">Tech With Tim</a><a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UC4JX40jDee_tINbkjycV4Sg" dir="auto">Tech With Tim</a>



#options = Options()
#options.headless = False

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = Chrome(options=option)
driver.implicitly_wait(5)
driver.get("https://youtube.com/")
time.sleep(10)
testList = driver.find_elements_by_class_name("yt-simple-endpoint.style-scope.yt-formatted-string")
print(type(testList))
print(len(testList))
print(testList[0].get_attribute("href"))
  

def isLink(tag):
	try:
		if tag['href'] != None:
			return True 
	except:
		return False

html = urlopen("https://www.wikipedia.org") 
obj1 = BeautifulSoup(html.read(),"lxml")
videoList = obj1.findAll(isLink)
print( 'wikipedia' +  videoList[0]['href'])
print(len(videoList))

def findName(tag):
	try:
		if tag['class'] == ['green']:
			return True
	except:
		return False
	return False
"""




