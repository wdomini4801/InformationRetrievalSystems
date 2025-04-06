import pandas as pd

file = pd.read_csv('polish_songs.csv')

result = file[(file['title'] == 'Nie zatrzymasz mnie')]

pd.set_option('display.max_colwidth', None)
print(result['lyrics'])
