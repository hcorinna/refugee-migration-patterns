import pandas
import os
import json

csv_input = 'unhcr_time_series_normalized.csv'
csv_output = 'migrate.json'
migration_filter = 'Refugees (incl. refugee-like situations)'

csv = pandas.read_csv(csv_input)

data = [
    row[['year', 'FROM', 'TO', 'value']].to_json()
    for index, row in csv.iterrows()
    if row['type'] == migration_filter
]

open(
    file=csv_output,
    mode='w+',
    encoding='utf-8'
).write(json.dumps(data))