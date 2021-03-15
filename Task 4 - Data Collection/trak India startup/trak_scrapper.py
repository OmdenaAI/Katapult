
from bs4 import BeautifulSoup       
import requests
import pandas as pd


URL = 'https://trak.in/india-startup-funding-investment-2015/'
content = requests.get(URL)
# content.status_code
soup = BeautifulSoup(content.text, 'html.parser')
# soup = BeautifulSoup(res.text,"lxml")
response = requests.get(URL)
text = soup.body.get_text()
# print(soup)

# <h2><span style="font-weight: bold;">Indian Startup Funding &amp; Investment Chart [2021]</span></h2>
# <p><h2 class="tablepress-table-name tablepress-table-name-id-55">February, 2021</h2>
# <table class="tablepress tablepress-id-55" id="tablepress-55">

# <h2 class="tablepress-table-name tablepress-table-name-id-55">February, 2021</h2>
more_data_urls = [URL]
year_wise_tables = []

for h3_tag in soup.find_all(name="h3"):
    more_data_urls.append(h3_tag.find(name='a').get('href'))

# for h2_tag in soup.find_all(name='h2'):
#     year_wise_tables.append(h2_tag.find(name='tablepress-table-name').get('class'))
#
#
# for url in year_wise_tables:
#     print(url)

# classes = []
# for i in range(0,56):
#     for element in soup.find_all(class_='tablepress-table-name tablepress-table-name-id-{i}'.format(i)):
#         classes.extend(element["class"])
# classes = set(classes)
# for c in classes:
#     print('hey',c)


new_row_list = []
column_name = ['Sr. No.', 'Date (dd/mm/yyyy)', 'Startup Name', 'Industry/ Vertical', 'Sub-Vertical', 'City / Location',
               'Investors’ Name', 'Investment Type', 'Amount (in USD)']
more_data_urls = set(more_data_urls)

urls_count = 1
for url in more_data_urls:
    html_response = requests.get(url)
    html_response.status_code
    soup = BeautifulSoup(html_response.content, 'html.parser')

    class_list = []
    for element in soup.find_all(class_=True):
        class_list.extend(element["class"])
    class_list = [cls for cls in class_list if 'tablepress-id-' in cls]
    # print(class_list)

    if len(class_list) < 1:
        skip_first_row = True
        class_list.append(None)
        for class_ in class_list:
            tbl = soup.find(name='table')  # , class_=class_)

            n_rows = 0
            for tr in tbl.find_all('tr'):
                if skip_first_row == True:
                    skip_first_row = False
                    continue
                new_row = {}
                for col_id, td in enumerate(tr.find_all('td')):
                    if col_id < len(column_name):
                        new_row[column_name[col_id]] = td.text
                if not new_row == {}:
                    n_rows += 1
                    new_row_list.append(new_row)
            # print("class_list-old:", class_, len(new_row_list), n_rows, url)
    else:
        for class_ in class_list:
            tbl = soup.find(name='table', class_=class_)

            n_rows = 0
            for tr in tbl.find_all('tr'):
                new_row = {}
                for col_id, td in enumerate(tr.find_all('td')):
                    if col_id < len(column_name):
                        new_row[column_name[col_id]] = td.text
                if not new_row == {}:
                    n_rows += 1
                    new_row_list.append(new_row)
            print("class_list-new :", class_, len(new_row_list), n_rows, url)

data = pd.DataFrame(new_row_list, columns=column_name)
data.to_csv('track_india_startups.csv')
print("Data shape :", data.shape)
print(data['Date (dd/mm/yyyy)'].value_counts())

# <h2 class="tablepress-table-name tablepress-table-name-id-31">January, 2019</h2>
