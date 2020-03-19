import json


def double_coefficient(data_json):

    # TODO: Refactor code: delete case when comparing the last
    #  two values, and have just one while loop!

    # Extract values from JSON
    data_values = list(data_json.values())

    coefficient_dict = dict()
    if data_values[-1] / data_values[-2] >= 2.0:
        coefficient = data_values[-1] / data_values[-2]
        coefficient_dict["start_double_date"] = \
            list(data_json.items())[-2][0]
        coefficient_dict["coefficient"] = \
            round(coefficient, 2)
        return coefficient_dict

    else:
        i = len(data_values) - 1
        while i >= 0:
            if data_values[-2] == data_values[i]:
                i -= 1
            else:
                if data_values[-1] / data_values[i] >= 2.0:
                    start_date_double = list(data_json.items())[i][0]
                    coefficient = data_values[-1] / data_values[i]
                    coefficient_dict["start_double_date"] = \
                        start_date_double
                    coefficient_dict["coefficient"] = \
                        round(coefficient, 2)
                    return coefficient_dict
                i -= 1


with open("data.json", "r+") as json_file:
    data = json.load(json_file)
    print(double_coefficient(data))
