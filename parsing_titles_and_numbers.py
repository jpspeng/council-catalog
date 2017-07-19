##### Pulling page in --------------

# modifying from
# http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
from bs4 import BeautifulSoup
#import urllib
#r = urllib.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()

import sys

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen

# Your code where you can use urlopen
with urlopen("http://sanjose.granicus.com/GeneratedAgendaViewer.php?event_id=fdfa3266-d7fa-40e3-84af-fa914c13e4e7") as url:
    agenda = url.read()

#print(agenda)

soup = BeautifulSoup(agenda, "html.parser")


###### get list of agenda item numbers --------------

# get all numbers and titles
titles_and_numbers = list(soup.find_all("td"))
# get just the item numbers markers
item_list = list(soup.find_all("td", class_="numberspace"))

start = 2
end = 4
count = 0
all_listings = []
while count <= len(item_list) + 1:
    item_listing = titles_and_numbers[start:end]
    start += 2
    end += 2
    count += 1
    if '<td class="numberspace"><strong>' not in str(item_listing):
        all_listings.append(item_listing)
    #all_listings.append(item_listing)

###### Parse out numbers and titles --------------

all_listings_noformat = []

for listing in all_listings:
    # convert to string to strip out HTML code
    i = str(listing)
    # strip out td class, but keep in <strong> so we can filter on it
    listed_number = i.replace('<td class="numberspace">', '').replace('</td>', '')     .replace('<br/>', '').replace(']', '').replace('<td>', '').replace('\r', '')     .replace('[', '').replace('\t', '').replace('\n', '').replace('\xa0', '')     .replace('       ', '').replace("'", '')
    # stripping out some other items that were picked up with <td>
    if '<td width="3%">' not in listed_number:
        all_listings_noformat.append(listed_number)

    
###### remove formatting --------------

# https://stackoverflow.com/questions/6903557/splitting-on-first-occurrence
item_holder = []

for listing in all_listings_noformat:
    listing_holder = []
    listing_holder = str(listing).split(" ", 1)
    listing_holder[0] = listing_holder[0].rstrip(', ')
    
    item_holder.append(listing_holder)
    

###### convert to dataframe and export as CSV
import pandas as pd

df = pd.DataFrame.from_records(item_holder, columns = ['item_num', 'item_title'])
print(df)
df.to_csv('agenda_titles_numbers.csv', index = False)