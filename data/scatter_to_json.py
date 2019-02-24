import pandas as pd
import json

pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv("country_year_features_merged.csv")

final_json = {}
for year in set(df['year']):
    filter_df = df[df['year'] == year]
    corr = json.loads(filter_df.to_json(orient='records'))
    final_json[year] = []
    for item in corr:
        del item['year']
        final_json[year].append(item)

open(
    file='../Visualization/src/data/scatter.json',
    mode='w+',
).write(json.dumps(final_json))
