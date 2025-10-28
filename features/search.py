import webbrowser
import urllib.parse
from config_files.config import search_engine
def search(query):
    query = query.replace("search", "").replace(search_engine, "").strip()
    if query:
        webbrowser.open(f"https://{search_engine}.com/search?q=" + urllib.parse.quote_plus(query))
    else:
        return "Please specify what you want to search for"
    return f"I found this on {search_engine}"