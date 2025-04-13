import matplotlib.pyplot as plt

percentage_data = [10, 20, 50, 75, 100]

es_time = [4.789, 9.484, 22.63, 34.676, 45.445]
solr_time = [4.481, 4.868, 10.548, 16.072, 23.022]
meili_time = [4.44, 4.28, 15.06, 23.73, 29.27]

es_size = [14.31, 30.06, 71.44, 93.64, 124.57]
solr_size = [13.68, 27.55, 68.37, 102.07, 135.01]
meili_size = [147.11, 222.07, 435.17, 641.7, 793.37]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# wykres 1: czas indeksowania vs procent danych
ax1.plot(percentage_data, es_time, marker='o', linestyle='-', label='ElasticSearch', color='blue')
ax1.plot(percentage_data, solr_time, marker='o', linestyle='-', label='Apache Solr', color='green')
ax1.plot(percentage_data, meili_time, marker='o', linestyle='-', label='Meilisearch', color='pink')

ax1.set_xlabel("Procent danych (%)")
ax1.set_ylabel("Czas indeksowania (S)")
ax1.set_title("Porównanie czasów indeksowania")
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.7)

# wykres 2: rozmiar indeksu vs procent danych
ax2.plot(percentage_data, es_size, marker='o', linestyle='-', label='ElasticSearch', color='blue')
ax2.plot(percentage_data, solr_size, marker='o', linestyle='-', label='Apache Solr', color='green')
ax2.plot(percentage_data, meili_size, marker='o', linestyle='-', label='Meilisearch', color='pink')

ax2.set_xlabel("Procent danych (%)")
ax2.set_ylabel("Rozmiar indeksu (MB)")
ax2.set_title("Porównanie rozmiarów indeksów")
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

plt.savefig("search_engine_comparison.png", dpi=300)

plt.show()
