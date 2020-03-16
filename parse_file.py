from bs4 import BeautifulSoup

with open('test_html/test.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

newsitem_inner = soup.find('div', class_='newsitem-inner')
text_center = newsitem_inner.find('div', class_='text_center')
paragraphs = text_center.find_all('p')

cases = [int(i) for i in paragraphs[1].text.split() if i.isdigit()]

print(cases[0])
