import meilisearch
from pprint import pprint

MEILI_URL = "http://localhost:7700"
MEILI_MASTER_KEY = None
INDEX_NAME = "repos"

try:
    print(f"\nConnecting with Meilisearch: {MEILI_URL}")
    client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)
    if not client.is_healthy():
        raise Exception("Meilisearch instance not available.")
    print("Connected successfully.")
    index = client.get_index(INDEX_NAME)

    search_query = ""
    filter_expression = 'Language = "Python"'

    print(f"\nWyszukiwanie dokumentów z filtrem: '{filter_expression}'")

    search_results = index.search(
        search_query,
        {
            'filter': filter_expression
        }
    )

    estimated_hits = search_results.get('estimatedTotalHits', 0)
    hits = search_results.get('hits', [])

    print(f"\nFound {estimated_hits} documents.")
    if hits:
        pprint(hits)
    else:
        print("No results.")

except Exception as e:
    print(f"Error: {e}")
    exit()

