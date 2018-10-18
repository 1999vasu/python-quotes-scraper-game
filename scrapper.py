import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

base_url = "http://quotes.toscrape.com"
page_url = "/page/1"
all_quotes = []
x = 0
while (page_url):
	
	res = requests.get(f"{base_url}{page_url}")
	soup = BeautifulSoup(res.text, 'html.parser')
	quotes = soup.find_all(class_ = "quote")
	
	for quote in quotes:
		all_quotes.append({
			"text": quote.find(class_ = "text").get_text(),
			"author": quote.find(class_ = "author").get_text(),
			"about_link": quote.find("a")["href"]
			})

	next = soup.find(class_ = "next")
	page_url = next.find("a")["href"] if next else None
	
	#Spacing out requests
	sleep(2)
	

with open('quotes.csv', 'a') as csv_file:
	writer = csv.writer(csv_file)
	for quote in all_quotes:
		writer.writerow([quote["text"], quote["author"], quote["about_link"]])
