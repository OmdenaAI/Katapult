from bs4 import BeautifulSoup
import requests
import time
import csv

url = "https://www.eu-startups.com/directory/"
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.content, "html.parser")

eu_startups = [] # country links
for link in soup.find_all('a', href=True):
    if 'https://www.eu-startups.com/directory/wpbdp_category/' in link['href'] and link['href'] not in eu_startups:
        eu_startups.append(link['href'])
print(eu_startups)

# ___________________________________________________________________________________


startup_country_wise = []

for country in range(len(eu_startups)):
    response_eu = requests.get(eu_startups[country])
    soup_eu = BeautifulSoup(response_eu.content, "html.parser")

    # get next url
    next_page_url = []
    for link in soup_eu.find_all(class_='next'):
        link = link.find('a', href=True)

        if 'https://www.eu-startups.com/directory/wpbdp_category/' in link['href']:
            next_page_url.append(link['href'])
    next_page_url = ' '.join([link for link in next_page_url])
    next_page_url = next_page_url.replace('2/', '')
    # next_page_url = "https://www.eu-startups.com/directory/wpbdp_category/austrian-startups/page/"

    i=1
    url = next_page_url+ str(i)
    while True:
        i = i + 1
        page = requests.get(url)
        soup_eu = BeautifulSoup(page.content, "html.parser")
        for link in soup_eu.find_all(class_='wpbdp-button button view-listing'):
            if 'https://www.eu-startups.com/directory/' in link['href']:
                # startup_country_wise['startups{}'.format(country + 1)].append(link['href'])
                startup_country_wise.append(link['href'])
        if page.status_code != 200:
            break
        url = next_page_url + str(i)


# print(startup_country_wise)

def scrape_info(url):

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        for item in soup.findAll(text='Business Name:'):
            try:
                business_name = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Category:'):
            try:
                country = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Business Description:'):

            try:
                business_description = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Based in:'):
            try:
                based_in = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Tags:'):
            try:
                tags = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Founded:'):
            try:
                founded = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Total Funding:'):
            try:
                total_funding = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text='Website:'):

            try:
                website = item.find_next('span').text
            except:
                pass

        for item in soup.findAll(text=re.compile('Articles')):
            for li in item.find_next('ul'):
                a = li.find('a')
                try:
                    if 'href' in a.attrs:
                        link = a.get('href')
                        articles.append(link)
                except:
                    pass

        articles = ','.join(articles)

        # saving this data in dictionary
        data = {'business_name': business_name, 'country': country, 'business_description': business_description,
                'based_in': based_in, 'tags': tags, 'founded': founded, 'total_funding': total_funding,
                'website': website, 'articles': articles}

        return data
    except:
        time.sleep(3)

   


# ------------------------------------------------------------------------------------------------------
temp = []
for url in startup_country_wise:
    temp.append(scrape_info(url))

import csv

f = open("eu_startup_data.csv", "w")
writer = csv.DictWriter(
    f, fieldnames=temp[0].keys())
writer.writeheader()
writer.writerows(temp)
f.close()



