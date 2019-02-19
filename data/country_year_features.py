import pandas as pd
from pandas import DataFrame
import numpy as np

import networkx as nx
import operator

pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("unhcr_time_series_normalized.csv")

# create df for asylum seekers
df_asylum = df[df['type']=="Asylum-seekers"]
out_asylumn_flows = df_asylum.groupby(["origin","year"])["value"].sum().reset_index().rename(columns={"origin":"country","value":"asylum_outflow"})
in_asylumn_flows = df_asylum.groupby(["destination","year"])["value"].sum().reset_index().rename(columns={"destination":"country","value":"asylum_inflow"})

# create df for refugees
df_refs = df[df['type']=="Refugees (incl. refugee-like situations)"]
outflows = df_refs.groupby(["origin","year"])[["value"]].sum().reset_index().rename(columns={"origin":"country","value":"outflow"})
inflows = df_refs.groupby(["destination","year"])["value","share"].sum().reset_index().rename(columns={"destination":"country","value":"inflow"})

iso = df_refs.groupby(["origin"])["iso-origin"].max().reset_index().rename(columns={"origin":"country","iso-origin":"iso"})

def year_measures(df,year,enable_graphing=False):
    # create network
    from_to_values = df.groupby(["origin", 'destination'])['value'].sum().reset_index().sort_values("value", ascending=False)
    edge_list = from_to_values[['origin', 'destination', 'value']]
    edges = list(map(tuple, list(edge_list.values)))
    DG = nx.DiGraph()
    DG.add_weighted_edges_from(edges)

    # create new df
    country_df = pd.DataFrame(np.array(list(set(list(df["origin"].unique()) + list(df["destination"].unique())))).reshape((-1,1)),columns=["country"])
    country_df["year"] = year

    # create out network
    to_from_values = df.groupby(["destination", 'origin'])['value'].sum().reset_index().sort_values("value", ascending=False)
    edge_list_out = to_from_values[["destination", 'origin', 'value']]
    edges_out = list(map(tuple, list(edge_list_out.values)))
    DG_out = nx.DiGraph()
    DG_out.add_weighted_edges_from(edges_out)

    # create undirected network
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    
    #######################################
    # clustering coefficient
    cc = nx.clustering(DG, weight=True)
    sorted_cc = sorted(cc.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_cc,columns=["country","clustering_coeff"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf,how="left",on="country")

    # number of triangles in the undirected graph
    tri = nx.triangles(G) # node level
    sorted_tri = sorted(tri.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_tri,columns=["country","sorted_tri"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # indegree centrality
    indegree_centrality = nx.algorithms.centrality.in_degree_centrality(DG)
    sorted_idc = sorted(indegree_centrality.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_idc,columns=["country","indegree_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # outdegree centrality
    outdegree_centrality = nx.algorithms.centrality.out_degree_centrality(DG)
    sorted_odc = sorted(outdegree_centrality.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_odc,columns=["country","outdegree_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # closeness centrality indegree
    closeness_centrality = nx.algorithms.centrality.closeness_centrality(DG)
    sorted_cc = sorted(closeness_centrality.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_cc,columns=["country","closeness_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # outdegree closeness centrality
    out_closeness_centrality = nx.algorithms.centrality.closeness_centrality(DG_out)
    sorted_cc_out = sorted(out_closeness_centrality.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_cc_out,columns=["country","out_closeness_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # betweenness centrality
    betweenness_centrality = nx.algorithms.centrality.betweenness_centrality(DG, normalized=True, weight=True)
    sorted_bc = sorted(betweenness_centrality.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_bc,columns=["country","betweenness_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # eigenvector centrality
    # indegree
    eigenvector_centrality = nx.eigenvector_centrality_numpy(DG, weight=True)
    sorted_ec = sorted(eigenvector_centrality.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_ec,columns=["country","eigenvector_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # outdegree eigenvector centrality
    eigenvector_centrality_out = nx.eigenvector_centrality_numpy(DG_out, weight=True)
    sorted_ec_out = sorted(eigenvector_centrality_out.items(), key=operator.itemgetter(1), reverse=True)
    ccdf = pd.DataFrame(sorted_ec_out,columns=["country","eigenvector_centrality_out"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # network constraint, long running time
#     print("-" * 10, "network constraint", "-" * 10)
    nxc = nx.algorithms.structuralholes.constraint(DG, weight="weight")
    sorted_nxc = sorted(nxc.items(), key=operator.itemgetter(1))
#     print(sorted_nxc)
    
    ccdf = pd.DataFrame(sorted_nxc,columns=["country","nxc"]).sort_values(["country"]).reset_index()
    country_df = country_df.merge(ccdf, how="left", on="country")
    return country_df
    

import time
df_year_measures = None
ts = time.time()
for year in sorted(df_refs["year"].unique()):
    df_refs_yr = df_refs[df_refs["year"]==year]
    
    dfm = year_measures(df_refs_yr,year)
    print(year,"|Time Taken %.1fs"%(time.time()-ts))
    ts = time.time()
    if df_year_measures is None:
        df_year_measures = dfm
    else:
        df_year_measures = pd.concat((df_year_measures,dfm),axis=0)


print(df_year_measures.shape)
df_year_measures = df_year_measures.merge(outflows,on=["country","year"],how="left")
df_year_measures = df_year_measures.merge(inflows,on=["country","year"],how="left")

df_year_measures = df_year_measures.merge(out_asylumn_flows,on=["country","year"],how="left")
df_year_measures = df_year_measures.merge(in_asylumn_flows,on=["country","year"],how="left")
df_year_measures = df_year_measures.merge(iso,on=["country"],how="left")

print(df_year_measures.shape)


wp = pd.read_csv("world_population_by_year.csv",skiprows=4)
wp = wp[["Country Code"]+list(map(str,range(2008,2018)))]
wp = wp.rename(columns={"Country Code":"iso"}).rename(columns=dict(zip(list(map(str,range(2008,2018))),list(range(2008,2018)))))


wp = pd.melt(wp, id_vars=["iso"], var_name="year", value_name="population")
#wp[wp["iso"]=="ABW"]

df_year_measures['year'] = df_year_measures['year'].astype(int)
wp['year'] = wp['year'].astype(int)
df_year_measures['iso'] = df_year_measures['iso'].astype(str)
wp['iso'] = wp['iso'].astype(str)

df_year_measures = df_year_measures.merge(wp,on=["iso","year"],how="left")

print(df_year_measures.shape)

# manual fixes for ISO
df_year_measures.loc[df_year_measures.country == 'Liechtenstein', 'iso'] = "LIE"
df_year_measures.loc[df_year_measures.country == 'Micronesia (Federated States of)', 'iso'] = "FSM"
df_year_measures.loc[df_year_measures.country == 'British Virgin Islands', 'iso'] = "VGB"
df_year_measures.loc[df_year_measures.country == 'Sint Maarten (Dutch part)', 'iso'] = "SXM"
df_year_measures.loc[df_year_measures.country == 'Aruba', 'iso'] = "ABW"

df_year_measures.to_csv("country_year_features_part10.csv",index=False)
