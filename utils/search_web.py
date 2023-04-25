import requests
from utils.keyword_extractor import extract_keywords

def search_web(extract_keywords):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": "AIzaSyDamub3bsg-99edgNp09Sz7nSonY-QQugU",
        "cx": "920802851d9cd44b2",
        "q": " ".join(extract_keywords),
        "num": 5
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to search the web (status code {response.status_code}): {response.text}")
    
    results = response.json().get("items", [])
    urls = [result["link"] for result in results]
    urls_string = "\n".join(urls) 
    
    return urls_string