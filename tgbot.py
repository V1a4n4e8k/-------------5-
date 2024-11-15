import pandas as pd
dict = {'href': [], 'title': [], 'image': []}
df = pd.DataFrame(dict)
df.to_csv('been_sent.csv', index_label='index')