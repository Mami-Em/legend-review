import requests

# /*
#   KITSU API:
#     * base:
#       -https://kitsu.io/api/edge
#       -https://kitsu.io/api/edge/anime/id

#     * search:
#       -https://kistu.io/api/edge/anime?filter[text]=title '%20'

#     * next page:
#       -"links": {
#         "first": "https://kitsu.io/api/edge/anime?page[limit]=5&page[offset]=0",
#         "next": "https://kitsu.io/api/edge/anime?page[limit]=5&page[offset]=5"
#       }

#     * sort:
#       -https://kitsu.io/api/edge/anime?sort=-startDate


#     * include
#       -https://kitsu.io/api/edge/anime/id?include=reviews
# */

query = requests.get("https://kitsu.io/api/edge/anime/11?include=reviews")
response = query.json()

print(response["data"]["id"])