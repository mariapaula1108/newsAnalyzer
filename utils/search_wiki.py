import requests

def search_wikipedia(keyword):
    API_URL = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "format": "json",
        "srsearch": keyword,
        "utf8": 1,
        "formatversion": 2
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        search_results = data["query"]["search"]
        return search_results
    else:
        print(f"Error {response.status_code}: Failed to fetch data from Wikipedia API")
        return []
