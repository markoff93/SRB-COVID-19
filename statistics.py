import json


# Function to return key for any value
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


with open("data.json", "r+") as json_file:
    data_json = json.load(json_file)

    # Extract keys and values from JSON
    data_keys = list(data_json.keys())
    data_values = list(data_json.values())

    if data_values[-1] / data_values[-2] >= 2.0:
        start_date_double = list(data_json.items())[-2][0]
        coefficient = data_values[-1] / data_values[-2]
        print(f"Broj slučajeva se povećao "
                     f"{round(coefficient,2)} puta \nod "
                     f"{list(data_json.items())[-2][0]}.")
    else:
        i = len(data_values)-1
        while i >= 0:
            if data_values[-2] == data_values[i]:
                i -= 1
            else:
                if data_values[-1] / data_values[i] >= 2.0:
                    start_date_double = list(data_json.items())[i][0]
                    coefficient = data_values[-1] / data_values[i]
                    print(f"Broj slučajeva se povećao "
                                 f"{round(coefficient,2)} puta od "
                                 f"{start_date_double}.")
                    break
                i -= 1
