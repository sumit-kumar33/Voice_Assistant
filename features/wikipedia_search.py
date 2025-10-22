from config_files.logs_config import *
import wikipedia

def wikipedia_search(query: str) -> str:
    try:
        query = query.replace("wikipedia", "").strip()
        if query:
            results = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {results}"
        else:
            return "Please specify what you want to search on Wikipedia"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific. Options include: {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic"
    except Exception as e:
        logging.exception(f"Wikipedia search error: {e}")
        return "Sorry, there was an error searching Wikipedia"