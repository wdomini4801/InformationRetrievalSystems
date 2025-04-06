import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import meilisearch
import math
from datetime import datetime
import gc

MEILI_URL = "http://localhost:7700"
MEILI_MASTER_KEY = None
INDEX_NAME = "songs"

songs = pd.read_csv('polish_songs.csv')
PRIMARY_KEY = 'id'
BATCH_SIZES = [5000, 10000, 20000, 40000, 60000, len(songs)]
MAX_BATCH_SIZE = 10000

print(f"\nPrimary key: '{PRIMARY_KEY}'")
columns_to_index = [PRIMARY_KEY, 'title', 'artist', 'tag', 'year', 'features', 'lyrics', 'language']

songs_subset = songs[columns_to_index]

print("\nCleaning data before converting to JSON...")

songs_cleaned = songs_subset.copy()
songs_cleaned = songs_cleaned.replace([np.inf, -np.inf], None)
songs_cleaned = songs_cleaned.replace([np.nan], [None])

documents = songs_cleaned.to_dict('records')
del songs_subset
del songs_cleaned
gc.collect()

if documents:
    print("\nFirst document to send (example):")
    print(documents[0])
else:
    print("\nDataFrame is empty, no documents.")
    exit()

if not all(PRIMARY_KEY in doc for doc in documents):
    print(f"\nERROR: Not all documents contain primary key: '{PRIMARY_KEY}'!")
    exit()

print(f"\nConnecting with Meilisearch: {MEILI_URL}")
try:
    client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)
    if not client.is_healthy():
        raise Exception("Meilisearch instance not available.")
    print("Connected successfully.")
except Exception as e:
    print(f"Error: {e}")
    exit()

index = client.get_indexes()['results']
if index:
    index = client.get_index(INDEX_NAME)
    print(f"Found existing index: '{INDEX_NAME}'")
    task = index.delete_all_documents()
    client.wait_for_task(task.task_uid)
    task = client.index(INDEX_NAME).delete()
    client.wait_for_task(task.task_uid)
    print("   Index and documents removed.")

task = client.create_index(INDEX_NAME, {'primaryKey': PRIMARY_KEY})
client.wait_for_task(task.task_uid)
index = client.get_index(INDEX_NAME)
print(f"Index '{INDEX_NAME}' created with primaryKey='{PRIMARY_KEY}'.")

# print("\nIndex configuration...")
# searchable_attributes = ['lyrics', 'title', 'artist']
# print(f"  Setting 'searchableAttributes': {searchable_attributes}")
# task = index.update_searchable_attributes(searchable_attributes)
# client.wait_for_task(task.task_uid, 30000)
# print("\nIndex configuration completed.")

doc_to_time = {}
doc_to_index = {}

for size in BATCH_SIZES:
    num_batches = math.ceil(size / MAX_BATCH_SIZE)
    start_time = 0
    end_time = 0
    print(f"Indexing {size} documents...")

    for i in range(num_batches):
        start_index = i * MAX_BATCH_SIZE
        end_index = start_index + size if num_batches == 1 else start_index + MAX_BATCH_SIZE
        batch = documents[start_index:end_index]
        print(f"    Indexing batch {i+1}/{num_batches} ({len(batch)} documents)...")
        try:
            if i == 0:
                start_time = datetime.now()
            task = index.update_documents(batch, primary_key=PRIMARY_KEY)
            client.wait_for_task(task.task_uid, 25000)
            if i == num_batches - 1:
                end_time = datetime.now()
                doc_to_index[size] = client.get_all_stats()['usedDatabaseSize']
        except Exception as e:
            print(f"  ERROR: {e}")

    doc_to_time[size] = (end_time - start_time).total_seconds()

sorted_doc_sizes = sorted(doc_to_time.keys())
times = [doc_to_time[size] for size in sorted_doc_sizes]
indexes = [doc_to_index[size] / (1024 * 1024) for size in sorted_doc_sizes]

print("\n--- Indexing Performance Summary ---")
print("Amount of docs | Indexing time (s) | Database size (MB)")
print("---------------|-------------------|-------------------")
for i, doc_size in enumerate(sorted_doc_sizes):
    indexing_time = round(times[i], ndigits=2)
    index_size = round(indexes[i], ndigits=2)
    print(f"{doc_size:<14} | {indexing_time:<17} | {index_size}")


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(sorted_doc_sizes, times, marker='o', linestyle='-', color='dodgerblue')
ax1.set_xlabel("Liczba dokumentów")
ax1.set_ylabel("Czas indeksowania (s)")
ax1.set_title("Czas indeksowania w zależności od liczby dokumentów")
ax1.grid(True, linestyle='--', alpha=0.7)

ax2.plot(sorted_doc_sizes, indexes, marker='s', linestyle='-', color='forestgreen')
ax2.set_xlabel("Liczba dokumentów")
ax2.set_ylabel("Rozmiar bazy danych (MB)")
ax2.set_title("Rozmiar bazy w zależności od liczby dokumentów")
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout(pad=3.0)
plt.show()
