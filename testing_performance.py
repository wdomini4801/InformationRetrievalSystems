from locust import HttpUser, task, between
import random

INDEX_NAME = "songs"
SEARCH_TERMS = ["miłość", "życie", "noc", "dzień", "polska", "tekst", "serce", "droga"]


class MeiliSearchUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def search_songs(self):
        query = random.choice(SEARCH_TERMS)
        search_payload = {
            "q": query,
            "limit": 10
        }

        # metoda POST dla wyszukiwania (zgodnie z rekomendacją Meilisearch)
        with self.client.post(f"/indexes/{INDEX_NAME}/search",
                              json=search_payload,
                              name=f"/indexes/{INDEX_NAME}/search",
                              catch_response=True) as response:
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if "hits" not in json_response:
                        response.failure(f"Invalid JSON response: Missing 'hits' key for query '{query}'")
                    else:
                        response.success()
                except ValueError:
                    response.failure(f"Invalid JSON response: Could not decode JSON for query '{query}'")
            else:
                response.failure(f"Status code {response.status_code} for query '{query}'")
