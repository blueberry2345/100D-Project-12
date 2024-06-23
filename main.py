import csv
from bs4 import BeautifulSoup
import requests

# Function that creates a list filled with a specific attribute for all the top audiobooks.
def get_attribute_list(attribute_html, text_start):
    attributes = [a.getText().strip()[text_start:].strip() for a in attribute_html]
    return attributes

# FUnction that gets the ratings of all the top audiobooks.
def get_ratings(ratings_html):
    ratings = []
    for r in ratings_html:
        rating = r.getText().strip().split()[0]
        if rating == "Not":
            rating = ""
        ratings.append(rating)
    return ratings



# Request html and parse.
stats_url = "https://www.audible.com/search?keywords=book&pageSize=50"
response = requests.get(stats_url)
stats_html = response.text
soup = BeautifulSoup(stats_html, "html.parser")
data = [["title", "author(s)", "length", "dates", "languages", "ratings"]]



# Get lists of all the relevant book attributes (title, author, length, date, languages and rating)
titles_html = soup.find_all(name="h3", class_="bc-heading bc-color-link bc-pub-break-word bc-size-medium" )
titles = get_attribute_list(titles_html, 0)

authors_html = soup.find_all(name="li", class_="bc-list-item authorLabel" )
authors = get_attribute_list(authors_html, 3)

lengths_html = soup.find_all(name="li", class_="bc-list-item runtimeLabel" )
lengths = get_attribute_list(lengths_html, 7)

dates_html = soup.find_all(name="li", class_="bc-list-item releaseDateLabel" )
dates = get_attribute_list(dates_html, 13)

languages_html = soup.find_all(name="li", class_="bc-list-item languageLabel" )
languages = get_attribute_list(languages_html, 9)

ratings_html = soup.find_all(name="li", class_="bc-list-item ratingsLabel" )
ratings = get_ratings(ratings_html)

# Create lists with the details of each audiobook then write to csv file.

for i in range(50):
    audiobook = [titles[i], authors[i], lengths[i], dates[i], languages[i], ratings[i]]
    data.append(audiobook)

with open("data/audiobooks.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)