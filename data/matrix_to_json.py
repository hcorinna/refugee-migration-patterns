import pandas as pd
from pandas import DataFrame
import numpy as np
import json
from matplotlib import pyplot as plt
import warnings

import networkx as nx
import operator

pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv("country_year_features_merged.csv")


df.hdi_value = df.hdi_value.astype(str)
df.hdi_value = df.hdi_value.str.replace(',','.')
df.hdi_value = df.hdi_value.astype(float)

df.hdi_rank = df.hdi_rank.astype(float)

df.fgi_rank = df.fgi_rank.astype(str)
df.fgi_rank = df.fgi_rank.str.replace('n','0')
df.fgi_rank = df.fgi_rank.str.replace('a','0')
df.fgi_rank = df.fgi_rank.astype(float)

df.fgi_value = df.fgi_value.astype(float)

df.hfi_value = df.hfi_value.astype(str)
df.hfi_value = df.hfi_value.str.replace('-','0')
df.hfi_value = df.hfi_value.astype(float)

df.hfi_rank = df.hfi_rank.astype(str)
df.hfi_rank = df.hfi_rank.str.replace('-','0')
df.hfi_rank = df.hfi_rank.astype(float)

final_json = {}

for year in set(df['year']):
    filter_df = df[df['year'] == year]
    corr = json.loads(filter_df.corr().to_json(orient='records'))
    final_json[year] = []
    for item in corr[1:]:
        del item['year']
        item['index'] = len(final_json[year])
        final_json[year].append(item)

open(
    file='../Visualization/src/data/matrix.json',
    mode='w+',
).write(json.dumps(final_json))
