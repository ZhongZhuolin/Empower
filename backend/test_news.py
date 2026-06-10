import requests

r = requests.get(
    "https://newsapi.org/v2/everything",
    params={"q": "apple", "pageSize": 1, "apiKey": "45fa5a862a9545c5ba477e72d3e694c1"}
)
print(r.json())
