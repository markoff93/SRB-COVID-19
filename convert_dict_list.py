import json

with open("emails.json", "r+") as json_emails:
    data_emails_dict = json.load(json_emails)

    print(list(data_emails_dict.values()))

