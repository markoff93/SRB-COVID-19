from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(filename='script.log', level=logging.DEBUG)

# Parse main page ------------------------------------------------------
source = requests.get('https://www.zdravlje.gov.rs/sekcija/'
                      '345852/covid-19.php').text

soup = BeautifulSoup(source, 'lxml')

page = soup.find('div', class_='page pagelang-sr')
news = page.find('div', class_='news')
container = news.find('div', class_='container-fluid blue-bg')
row = container.find('div', class_='row')
col_sm_8 = row.find('div', class_='col-sm-8')
nl_wrapper = col_sm_8.find('div', class_='nl-wrapper')
list_unstyled = nl_wrapper.find('ul', class_='list-unstyled news-list')

list_news = list_unstyled.find_all('li')

news_text = list()
for item in list_unstyled.find_all('li'):
    new = item.find('div', class_='news-text')
    news_text.append(new)

h1s = list()
for h1 in news_text:
    h1s.append(h1.find('h1', class_="press-title"))

hrefs = list()
for href in h1s:
    hrefs.append(href.find('a', href=True))

links = list()
for a in hrefs:
    links.append("https://www.zdravlje.gov.rs/" + a['href'])

# Parse links from main page -------------------------------------------
source_link = requests.get(links[0]).text

soup_link = BeautifulSoup(source_link, 'lxml')

page_pagelang_sr = soup_link.find('div', class_='page pagelang-sr')
news_article = page_pagelang_sr.find('div', class_='news-article')
containers = news_article.find('div', class_='container-fluid blue-bg')
row_link = containers.find('div', class_='row')
col_sm_8_link = row_link.find('div', class_='col-sm-8 col-lg-10 '
                                            'white-bg nl-wrapper')
newsitem_inner = col_sm_8_link.find('div', class_='newsitem-inner')
tts_content = newsitem_inner.find('div', class_='tts-content')

# Check if there is 'Информације' substring in h1 class col-xs-12
if "Информације" in tts_content.find('h1', class_='col-xs-12').text:
    logging.info("There IS new information about the COVID-19!")
    row_tts_link = tts_content.find('div', class_='row')
    text_covid19 = row_tts_link.p.text
    try:
        start_index = text_covid19.index("регистровано укупно")
        end_index = text_covid19.index("потврђених")

        cases = text_covid19[start_index+20:end_index]
        print(int(cases))
    except ValueError:
        logging.error("Couldn't find 'регистровано укупно' or"
                      "'потврђених' string!")

else:
    logging.info("There is NO new information about the COVID-19!")


# print(row_tts_link.p.text)
# print(tts_content)
