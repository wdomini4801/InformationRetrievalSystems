import pandas as pd
import gc

file_path = '/Users/wdomi/Downloads/song_lyrics.csv'
chunk_size = 100000
processed_chunks = []

chunk_iterator = pd.read_csv(
    file_path,
    chunksize=chunk_size
)

for i, chunk in enumerate(chunk_iterator):
    print(f"Processing {i + 1} chunk...")

    polish_lyrics_chunk = chunk[chunk['language'] == 'pl'].copy()

    if not polish_lyrics_chunk.empty:
        processed_chunks.append(polish_lyrics_chunk)
        print(f"   Found {len(polish_lyrics_chunk)} polish songs in chunk {i + 1}.")
    else:
        print(f"   No polish songs in chunk {i + 1}.")

    del chunk
    gc.collect()

print("\nFile processed.")

if processed_chunks:
    final_df = pd.concat(processed_chunks, ignore_index=True)
    print(f"\nCreated file with {len(final_df)} polish songs.")
    final_df.to_csv('polish_songs.csv', index=False)
else:
    print("\nNo polish songs in file.")
