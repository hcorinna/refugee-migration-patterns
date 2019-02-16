import pandas as pd
import os
import json

csv_input = 'unhcr_time_series_normalized.csv'
csv_output = '../Visualization/src/data/migrate.json'

# we can discuss if we want to use a slider for "type" to include IDP etc
migration_filter = 'Refugees (incl. refugee-like situations)' 

csv = pd.read_csv(csv_input)

data = [
    row[['year', 'iso-origin', 'iso-destination', 'value', 'share']].to_json()
    for index, row in csv.iterrows()
    if row['type'] == migration_filter
]

open(
    file=csv_output,
    mode='w+',
    encoding='utf-8'
).write(json.dumps(data))