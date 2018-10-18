import csv
import requests
from bs4 import BeautifulSoup
from random import choice

base_url = "http://quotes.toscrape.com"

def get_all_quotes():
	all_quotes = []
	#Reading all the quotes from the csv file and storing in all_quotes
	try:
		with open('quotes.csv', 'r') as csv_file:
			reader = csv.reader(csv_file)
			for quote in reader:
				all_quotes.append({
					"text": quote[0],
					"author": quote[1],
					"about_link": quote[2]
					})
		return all_quotes
	except IOError:
		print("Something went wrong could not find or read the csv file!")
		exit(0)

def get_hints(quote):
	hints = []

	#Getting hints for the question from the about page of the author
	res = requests.get(f"{base_url}{quote['about_link']}")
	soup = BeautifulSoup(res.text, "html.parser")

	#Date of birth and location of the author
	born_on = soup.find(class_ = "author-born-date").get_text()
	born_location = soup.find(class_ = "author-born-location").get_text()
	hint_born = f"The author was born on {born_on} {born_location}"
	hints.append(hint_born)

	#Initials of the author
	initials = ' '.join(x[0] for x in quote["author"].split(" "))
	hint_initials = f"The initials of the author are {initials}"
	hints.append(hint_initials)
	
	return hints


def startGame(all_quotes):
	selected_quote = choice(all_quotes)
	num_guesses = 3
	hints = get_hints(selected_quote)

	print("\n",selected_quote["text"], "\n")
	
	while(num_guesses > 0):
		print("Number of guesses left: ", num_guesses)
		answer = input("Answer: ")
		if(answer.lower() == selected_quote["author"].lower()):
			print("\nCorrect answer!\n")
			break
		
		num_guesses -= 1
		if (num_guesses > 0):
			print(f"\nhint: {hints[2 - num_guesses]}\n")
	else:
		print("You're out of guesses! The correct answer is ", selected_quote["author"])

def main():
	try:
		all_quotes = get_all_quotes()
		print("Guess the author of the following famous quote!")
		op = 'y'
		while(op == 'y'):
			startGame(all_quotes)
			op = input("do you want to play again?(y/n): ")
			while(op not in ['y', 'n']):
				print("please enter valid option!")
				op = input("Do you want to play again?(y/n): ")
	
	except KeyboardInterrupt:
		print("\nYou quit the game!")
	
	finally:
		print("Thanks for playing :D")

if __name__ == "__main__":
	main()