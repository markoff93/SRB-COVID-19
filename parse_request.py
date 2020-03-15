from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.zdravlje.gov.rs/vest/346492/'
                      'informacije-o-novom-korona-1503-u-8-'
                      'casova.php').text

soup = BeautifulSoup(source, 'lxml')

newsitem_inner = soup.find('div', class_='newsitem-inner')
text_center = newsitem_inner.find('div', class_='text_center')
paragraphs = text_center.find_all('p')

cases = [int(i) for i in paragraphs[1].text.split() if i.isdigit()]

print(cases[0])
