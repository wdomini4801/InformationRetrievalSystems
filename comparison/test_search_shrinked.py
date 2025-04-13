import meilisearch
import json
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

    search_query = "interview OR computer-science OR python"
    # search_query = ''
    # filter_expression = "Stars > 150000"
    # filter_expression = 'Topics IN ["interview", "computer-science", "python"]'

    print(f"\nSearching documents with query: '{search_query}'")

    search_results = index.search(
        search_query,
        {
            # 'filter': filter_expression,
            'attributesToSearchOn': ['Topics']
        }
    )

    estimated_hits = search_results.get('estimatedTotalHits', 0)
    hits = search_results.get('hits', [])

    print(f"\nFound {estimated_hits} documents.")
    if hits:
        pprint(hits)
    else:
        print("No results.")

    OUTPUT_FILENAME = "topics.json"

    if hits:
        print(f"Saving documents to file: {OUTPUT_FILENAME}")
        try:
            with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
                json.dump(hits, f, ensure_ascii=False, indent=4)
            print("Saved.")
        except IOError as e:
            print(f"Error: cannot save to file: {OUTPUT_FILENAME}: {e}")
        except Exception as e:
            print(f"ERROR while saving to JSON: {e}")
    else:
        print("No documents to save.")


except Exception as e:
    print(f"Error: {e}")
    exit()

