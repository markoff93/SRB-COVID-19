import json
from datetime import date

with open('data.json', 'r+') as json_file:
    data = json.load(json_file)

    data_list = list((data.items()))
    last_value = int(data_list[-1][-1])

    today = date.today()
    day = str(today).split('-')[-1]
    print(day)
