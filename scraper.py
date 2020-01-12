## ncurses style ASCII banner library
import pyfiglet
## packages for NLP
import nltk
from nltk.corpus import stopwords
## packages for scraping
import requests
from bs4 import BeautifulSoup
## to use for autocorrect
from autocorrect import Speller

banner = pyfiglet.figlet_format("Fake News Shall Quiver")
print(banner)

## URLs of sources
reuters = "https://www.reuters.com/search/news?sortBy=&dateRange=&blob="
bbc = "https://www.bbc.co.uk/search?q="

## previously manually entered keywords
# keywords = input("Enter Keywords:").split()
# search_string = keywords[0]

spell = Speller(lang='en')

## parsing though user's query to generate effective query
user_query = input("What Shall We Check Pour Vous?\n").lower().replace("?","")
print("\nChecking Against Sources!")

spellize = nltk.word_tokenize(user_query)
for w in spellize:
    w = spell(w)

words = nltk.chunk.ne_chunk(nltk.pos_tag(spellize))

stop_words = set(stopwords.words('english'))
query = []

for w in words:
    if len(w) == 1:
        query.append(w)
        continue
    if w[1] != 'DT' and w[0] not in stop_words:
        query.append(w[0])

query = ' '.join(query)

## Sending requests to sources and scraping article summaries
r1 = requests.get(reuters+query)
r2 = requests.get(bbc+query)

reuters_content = r1.content
bbc_content = r2.content
all_arts = []

soup1 = BeautifulSoup(reuters_content, 'lxml')
reuters_topics = soup1.find_all('div', class_="search-result-content")

soup2 = BeautifulSoup(bbc_content, 'lxml').find_all('article')
bbc_headlines = [ex for ex in (sub.find('h1', itemprop="headline") for sub in soup2) if ex]
bbc_topics = [ex for ex in (sub.find('p', class_="summary long") for sub in soup2) if ex]
bbc_search = []
for i in range(len(bbc_headlines)-1):
    all_arts.append((bbc_headlines[i].get_text()+bbc_topics[i].get_text()).replace("\n"," ").replace("…"," ").replace("'s","").replace(":","").lower().split())

## test how many articles contain the keywords

for t in reuters_topics:
    all_arts.append(t.get_text().lower().replace("'s","").replace(":","").split())

count = [0] * len(all_arts)

for i in range(len(all_arts)):
    if(all(e in all_arts[i] for e in query.split())):
        count[i] = 1
       
## now return the ratio of successful hits
if(len(count) != 0):
    ratio = (sum(count[:])/len(count))
    if ratio < 0.5:
        print("Likely untrue")
    elif ratio < 0.7:
        print("Potentially true")
    else:
        print("Very likely true")
else:
    print("Not enough data! Likely false!")


