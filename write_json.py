import json

data = {"6. \nMarch": 1, "9. \nMarch": 2, "10. \nMarch": 5,
        "11. \nMarch": 18, "12. \nMarch": 24, "13. \nMarch": 35,
        "14. \nMarch": 46, "15. \nMarch": 48, "16. \nMarch": 57}

with open('data.json', 'w') as f:
    json.dump(data, f)