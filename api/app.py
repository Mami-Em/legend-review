import requests

query = requests.get("https://kitsu.io/api/edge/anime/11?include=reviews")
response = query.json()

print(response["data"]["id"])