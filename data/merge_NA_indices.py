import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import warnings
warnings.filterwarnings('ignore')

df_year_measures = pd.read_csv("country_year_features.csv")

im = pd.read_csv("indices_merged_iso_updated.csv")
im = im[['year','hdi_value', 'iso', 'hdi_rank', 'fgi_rank', 'fgi_value', 'hfi_rank', 'hfi_value']]
df_year_measures = df_year_measures.merge(im,on=["iso","year"],how="left")


df_year_measures.to_csv("country_year_features_merged.csv",index=False)

