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
"""
CSV to 2D array
results = []
with open("input.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        results.append(row)

"""

#Functions
def cleanDate(string):
	res = string[:len(string) - 1]
	arr = res.split('T')
	return arr


def reverse(string):
    string = string[::-1]
    return string

def getRepoName(string):
	i = len(string) - 1 
	res = ''
	while i>=0:
		if string[i] =='/':
			break
		res = res + string[i]
		i = i - 1 
	return reverse(res)

def getCreator(string):
	res = ''
	for i in range(19,len(string)):
		if string[i] == '/':
			break
		else:
			res = res + string[i]
	return res

#Step 1: Load the page and store the links

url = 'https://github.com/search?q='
print("Enter The Topic:")
url = url + input()

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver1  = Chrome(options = option)
driver1.implicitly_wait(5)

driver1.get(url)
time.sleep(1)
repo_list = driver1.find_elements_by_class_name("v-align-middle")
repo_links = list()
for item in repo_list:
	if item.get_attribute("href"):
		repo_links.append(item.get_attribute("href"))
	else:
		pass
pprint(repo_links)

#Step 2: Load individual links and get the required data from each page 
complete_info = []
repo_name = list()
repo_creator = list()
for url in repo_links:

	driver2  = Chrome(options = option)
	driver2.get(url)
	time.sleep(0.5)

	name = str(getRepoName(url))
	creator = str(getCreator(url))
	star_list = driver2.find_elements_by_class_name("social-count.js-social-count")
	fork_list = driver2.find_elements_by_class_name("social-count")
	date_list = driver2.find_elements_by_class_name('no-wrap')
	language_info = driver2.find_elements_by_class_name("color-text-primary.text-bold.mr-1")
	languages = []
	for item in language_info:
		try:
			languages.append(str(item.text))
		except:
			pass
	for item in date_list:
		if item.get_attribute("datetime")!=None:
			p = cleanDate(str(item.get_attribute("datetime")))
			date = str(p[0])
			times = str(p[1])
			break
		else:
			pass 

	stars = (star_list[0].text)
	forks = (fork_list[1].text)

	languages_s = ','.join(languages)
	complete_info.append([name,creator,url,stars,forks,date,times,languages_s ])

complete_info = [['Repository Name' , 'Creator','Url','Stars','Forks','Date of Creation','Time of Creation','Languages']] + complete_info
with open("github.csv", "w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(complete_info)