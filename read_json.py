import json
import matplotlib.pyplot as plt

with open('data.json') as json_file:
    data = json.load(json_file)

    plt.bar(range(len(data)),
            list(data.values()),
            align='center')
    plt.xticks(range(len(data)),
               list(data.keys()))

    plt.savefig("mygraph_from_json.png")