import os
import json
import ssl
import smtplib
import logging
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests

# Setup logging to a file
logging.basicConfig(filename='main.log', level=logging.INFO,
                    filemode='w')


def send_emails(day_subject):
    # Prompt for correct input
    while True:
        json_to_parse = str(input(
            "Enter the name of JSON file with the "
            "list of emails (TEST: emails.json or "
            "PROD: emails_all.json): "))
        if json_to_parse == "emails.json" or \
                json_to_parse == "emails_all.json":
            break

    # Read email list
    with open(json_to_parse, "r+") as json_emails:

        # Load JSON file
        data_emails_dict = json.load(json_emails)

        # Define email content and require the password
        subject = f"SRB COVID-19 izveštaj na dan {day_subject}. " \
                  f"mart 2020."
        body = "Izveštaj se nalazi u prilogu."
        sender_email = "covid19.srb@gmail.com"
        receiver_email = list(data_emails_dict.values())
        password = input("Type your password and press enter:")

        # Create a multipart message and set subject
        message = MIMEMultipart()
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Open image
        filename = "Poslednji_izveštaj.png"
        img = open(filename, 'rb')
        img_data = img.read()
        image = MIMEImage(img_data, name=os.path.basename(filename))

        # Add attachment to message and convert message to string
        message.attach(image)
        text = message.as_string()

        # Log in to server using secure context and send emails
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=context) as server:
            server.login(sender_email, password)
            for email in receiver_email:
                server.sendmail(sender_email, email, text)

        # Close image
        img.close()


def double_coefficient(data_json):
    # Extract values from JSON
    data_values = list(data_json.values())

    # Determine coefficient and start_double_date
    coefficient_dict = dict()
    i = len(data_values) - 1
    while i >= 0:
        if data_values[-1] / data_values[i] >= 2.0:
            start_date_double = list(data_json.items())[i][0]
            coefficient = data_values[-1] / data_values[i]
            coefficient_dict["start_double_date"] = \
                start_date_double
            coefficient_dict["coefficient"] = \
                round(coefficient, 2)
            return coefficient_dict
        else:
            i -= 1


# Parse news page
# TODO: Refactor the for loops: item, h1, and href!!!
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

# Get list of links from news page
links = list()
for a in hrefs:
    links.append("https://www.zdravlje.gov.rs/" + a['href'])

# Get page from latest link and parse latest page
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

# Check if there is 'Информације' substring in headline
if "Информације" in tts_content.find('h1', class_='col-xs-12').text:
    logging.info("There IS new information about the COVID-19!")
    row_tts_link = str(tts_content.find('div', class_='row').text)

    try:
        start_index = row_tts_link.index("укупно")
        end_index = row_tts_link.index("потврђен")
        cases = int(row_tts_link[start_index+7:end_index])

        with open("data.json", "r+") as json_file:
            data = json.load(json_file)

            data_list = list((data.items()))
            last_value = int(data_list[-1][-1])

            if cases != last_value:
                # Update JSON
                logging.info("New number of cases to append to JSON!")
                today = date.today()
                day = str(today).split('-')[-1]
                to_append = {f"{day}. \nmart": cases}
                data.update(to_append)
                json_file.seek(0)
                json.dump(data, json_file, indent=2)
                logging.info("Successfully updated JSON!")

                # Visualize
                logging.info("Visualizing ...")
                bar = plt.bar(range(len(data)), list(data.values()),
                              align='center')
                plt.xticks(range(len(data)), list(data.keys()))
                plt.tick_params(axis='x', which='major', labelsize=7)
                plt.ylabel('Broj zaraženih')
                plt.suptitle(f'SRB COVID-19 izveštaj na dan {day}.'
                             f' mart 2020.', fontsize=12,
                             fontweight='bold')
                # TODO: Fix text_top_h value generation
                text_top_h = int(cases) - 20
                plt.text(0, text_top_h, f'Broj novozaraženih osoba \nu '
                                        f'odnosu na {int(day)-1}. mart:'
                                        f'\n+{cases - last_value}',
                                        fontsize=8, fontweight='bold')
                for rect in bar:
                    height = rect.get_height()
                    plt.text(rect.get_x() + rect.get_width()/2.0,
                             height, '%d' % int(height), ha='center',
                             va='bottom')

                # Determine coefficient of duplication
                determine_coeff_dict = double_coefficient(data)
                double_date = str(determine_coeff_dict[
                                      "start_double_date"]).replace(
                    '\n', '')
                double_date_number_list = [int(i) for i in
                                           double_date.split(".") if
                                           i.isdigit()]
                double_date_number = int(double_date_number_list[0])

                double_coeff = determine_coeff_dict["coefficient"]
                # TODO: Fix text_bottom_h value generation
                text_bottom_h = text_top_h - 45
                plt.text(0, text_bottom_h,
                         f"Broj slučajeva se povećao "
                         f"{double_coeff} puta \nu poslednja "
                         f"{int(day)-double_date_number} "
                         f"dana (od {double_date}a)."
                         , fontsize=8, fontweight='bold'
                         )
                plt.savefig("Poslednji_izveštaj.png")
                logging.info("Successfully visualized JSON data!")

                # Send emails
                logging.info("Sending emails ...")
                send_emails(day)
                logging.info("Emails are sent!")
            else:
                logging.info("No new number of cases "
                             "to append to JSON!")
    except ValueError:
        logging.error("Couldn't find 'регистровано укупно' or"
                      "'потврђен' substring!")

else:
    logging.info("There is NO new information about the COVID-19!")
