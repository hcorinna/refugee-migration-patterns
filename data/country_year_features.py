from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import pandas as pd
from pandas import DataFrame
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns
import networkx as nx
import powerlaw
import operator

import missingno as msno


pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("unhcr_time_series_normalized.csv")
df.head()


df_asylum = df[df['type']=="Asylum-seekers"]
df_asylum.head()

out_asylumn_flows = df_asylum.groupby(["origin","year"])["value"].sum().reset_index().rename(columns={"origin":"country","value":"asylum_outflow"})
in_asylumn_flows = df_asylum.groupby(["destination","year"])["value"].sum().reset_index().rename(columns={"destination":"country","value":"asylum_inflow"})



df_refs = df[df['type']=="Refugees (incl. refugee-like situations)"]
df_refs.head()

outflows = df_refs.groupby(["origin","year"])[["value"]].sum().reset_index().rename(columns={"origin":"country","value":"outflow"})
inflows = df_refs.groupby(["destination","year"])["value","share"].sum().reset_index().rename(columns={"destination":"country","value":"inflow"})
iso = df_refs.groupby(["origin"])["iso-origin"].max().reset_index().rename(columns={"origin":"country","iso-origin":"iso"})


def draw_weighted_graph(G,title,percentiles={"high":95,"mid":60,"low":40},label_edge=False):
    
    df = pd.DataFrame(index=G.nodes(), columns=G.nodes())
    for row, data in nx.shortest_path_length(G):
        for col, dist in data.items():
            df.loc[row,col] = dist

    df = df.fillna(df.max().max())
    
    dists = {}
    for edge in G.edges():
        inv = int(10/np.sqrt(np.log1p(G.edges[edge]["weight"])))
        dists[edge] = inv
    
    
    all_weights = [G.edges[edge]["weight"] for edge in G.edges]
    percentiles = {k:np.percentile(all_weights,v) for k,v in percentiles.items()}
    
    edge_labels = {}
    edge_lists = {}
    edge_lists = {k:list() for k in percentiles.keys()}
    high = list()
    mid = list()
    low = list()
    
    for edge in G.edges():
        w = G.edges[edge]["weight"]
        edge_labels[edge] = G.edges[edge]["weight"]
        if w>=percentiles["high"]:
            high.append(edge)
        elif w>=percentiles["mid"] and w<percentiles["high"]:
            mid.append(edge)
        elif w>=percentiles["low"] and w<percentiles["mid"]:
            low.append(edge)
        else:
            pass
    edge_lists = {"high":high,"mid":mid,"low":low}
    
    print(len(high),len(G.edges()))

    
    
    plt.figure(figsize=(16, 16));
    plt.title(title)
    pos = nx.random_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos,font_size=12)
    if label_edge:
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='red')
    
        
    # nx.draw_networkx_edges(G, pos, width=0.2, alpha=0.2)
    nx.draw_networkx_edges(G, pos,edgelist=edge_lists["high"],width=1, alpha=0.9, edge_color='black')
    # nx.draw_networkx_edges(G, pos,edgelist=edge_lists["mid"],width=0.5, alpha=0.5, edge_color='green')
    # nx.draw_networkx_edges(G, pos,edgelist=edge_lists["low"],width=0.25, alpha=0.25, edge_color='lightgreen')
    plt.axis('off')
    plt.show()
    

from_to_values = df_refs[df_refs["year"]==2017].groupby(["origin", 'destination'])['value'].sum().reset_index().sort_values("value", ascending=False)
edge_list = from_to_values[['origin', 'destination', 'value']]
edges = list(map(tuple, list(edge_list.values)))
DG = nx.DiGraph()
DG.add_weighted_edges_from(edges)


## function to call each year
def graphing_and_diagnostics(df,G,DG,DG_out,year):
    draw_weighted_graph(DG,"DiGraph of Refugees Flow year=%s"%year)
    draw_weighted_graph(DG_out,"DiGraph of Out Flows year=%s"%year)
    
    ## plot powerlaw
    # outdegree powerlaw
    origin = df.groupby(["origin"])["value"].agg(['sum'])
    origin = origin.sort_values(['sum'], ascending=False)
    degree_values = origin['sum'].tolist()  # sorted(set(degrees.values()))
    
    plt.figure(figsize=(18, 8));
    fit = powerlaw.Fit(np.array(degree_values) + 1, xmin=1, discrete=False)
    fit.power_law.plot_ccdf(color='b', linestyle='--', label='fit ccdf')
    fit.plot_ccdf(color='r')
    plt.title('Outdegree powerlaw: Origin of Refugees year=%s'%year) # add year to title
    plt.xlabel('Out k = Number of refugees')
    plt.ylabel('Complementary CDF ' + r'$P(X\geq k)$')
    # plt.legend(lables, loc='best', fontsize = 'small')
    plt.show()
    print('alpha= ', fit.power_law.alpha, '  sigma= ', fit.power_law.sigma)
    
    # indegree powerlaw
    destination = df.groupby(["destination"])["value"].agg(['sum'])
    destination = destination.sort_values(['sum'], ascending=False)
    degree_values = destination['sum'].tolist()  # sorted(set(degrees.values()))

    plt.figure(figsize=(18, 8));
    # lables = [r'$x^{-( \alpha-1)}, \alpha = 1.11$', "Empirical data"]
    fit = powerlaw.Fit(np.array(degree_values) + 1, xmin=1, discrete=False)
    fit.power_law.plot_ccdf(color='b', linestyle='--', label='fit ccdf')
    fit.plot_ccdf(color='r')
    plt.title('Indegree powerlaw: Destination of Refugees year=%s'%year)
    plt.xlabel('In k = Number of refugees')
    plt.ylabel('Complementary CDF ' + r'$P(X\geq k)$')
    # plt.legend(lables, loc='best', fontsize = 'small')
    plt.show()
    print('alpha= ', fit.power_law.alpha, '  sigma= ', fit.power_law.sigma)
    
    # basic characteristics of the network
    num_nodes = len(DG)
    e_max = num_nodes * (num_nodes - 1) / 2
    num_edges = DG.number_of_edges()
    deg_k = num_edges / num_nodes
    print("num_nodes: ", num_nodes)
    print("num_edges: ", num_edges)
    print("e_max: ", e_max) # max possible number of edges
    print("deg_k: ", deg_k) # average degree k
    
    # clustering coefficient
    print("average_clustering = %.4f"%nx.average_clustering(DG, weight=True))  # year level
    print("average_clustering out = %.4f"%nx.average_clustering(DG_out, weight=True))  # year level
    
    ## Degree Distribution indegree
    inflow = df.groupby(['destination'])['value'].sum().reset_index().sort_values("value", ascending=False)
    inflow_values = inflow.value.tolist()
    plt.figure(figsize=(12,10))
    plt.hist(inflow_values, density=True, log=True,bins=50)
    plt.title("Incoming Refugees Histogram year=%s"%year)
    plt.ylabel("Probability of degree k")
    plt.xlabel("Degree k")
    


    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.show()

    ## Degree distribution outdegree
    outflow = df.groupby(['origin'])['value'].sum().reset_index().sort_values("value", ascending=False)
    outflow_values = outflow.value.tolist()
    plt.figure(figsize=(12,10))
    plt.hist(outflow_values, density=True, log=True,bins=50)
    plt.title("Outgoing Refugees Histogram year=%s"%year)
    plt.ylabel("Probability of degree k")
    plt.xlabel("Degree k")
    

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)

    plt.show()
    
    origin = origin.reset_index().rename(columns={"origin":"country","sum":"outgoing"})
    destination = destination.reset_index().rename(columns={"destination":"country","sum":"incoming"})
    
    origin = origin.merge(destination,how="inner",on="country").sort_values(["outgoing"])
    origin = origin.sort_values(by="outgoing").reset_index()
    
    plt.figure(figsize=(18,6))
    plt.xticks(rotation=90)
    plt.title("Outgoing vs Incoming count: Sorted by outgoing year=%s"%year)
    plt.plot(origin.country,origin.incoming,label="Incoming")
    plt.plot(origin.country,origin.outgoing,label="Outgoing")
    plt.xlabel("Country")
    plt.ylabel("Counts");
    plt.semilogy()
    plt.legend()
    
    plt.show()
    
    origin = origin.sort_values(by="incoming").reset_index()
    
    plt.figure(figsize=(18,6))
    plt.xticks(rotation=90)
    plt.title("Outgoing vs Incoming count: Sorted by Incoming year=%s"%year)
    plt.plot(origin.country,origin.incoming,label="Incoming")
    plt.plot(origin.country,origin.outgoing,label="Outgoing")
    plt.xlabel("Country")
    plt.ylabel("Counts");
    plt.semilogy()
    plt.legend()
    
    plt.show()




def year_measures(df,year,enable_graphing=False):
    # plot network
    from_to_values = df.groupby(["origin", 'destination'])['value'].sum().reset_index().sort_values("value", ascending=False)
    edge_list = from_to_values[['origin', 'destination', 'value']]
    edges = list(map(tuple, list(edge_list.values)))
    DG = nx.DiGraph()
    DG.add_weighted_edges_from(edges)
    
    
    country_df = pd.DataFrame(np.array(list(set(list(df["origin"].unique()) + list(df["destination"].unique())))).reshape((-1,1)),columns=["country"])
    country_df["year"] = year
    # plot out network
    to_from_values = df.groupby(["destination", 'origin'])['value'].sum().reset_index().sort_values("value", ascending=False)
    edge_list_out = to_from_values[["destination", 'origin', 'value']]
    edges_out = list(map(tuple, list(edge_list_out.values)))
    DG_out = nx.DiGraph()
    DG_out.add_weighted_edges_from(edges_out)
    

    # create undirected network
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    
    #######################################
    
    if enable_graphing:
        graphing_and_diagnostics(df,G,DG,DG_out,year)

    # print("-"*10, "clustering coefficient", "-"*10)
    cc = nx.clustering(DG, weight=True)
    sorted_cc = sorted(cc.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_cc)  # node level
    ccdf = pd.DataFrame(sorted_cc,columns=["country","clustering_coeff"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf,how="left",on="country")

    

    # number of triangles in the undirected graph
    # print("-"*10, "number of triangles", "-"*10)
    tri = nx.triangles(G) # node level
    sorted_tri = sorted(tri.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_tri)
    ccdf = pd.DataFrame(sorted_tri,columns=["country","sorted_tri"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")
    

    

    # indegree centrality
    # print("-" * 10, "indegree centrality", "-" * 10)
    indegree_centrality = nx.algorithms.centrality.in_degree_centrality(DG)
    sorted_idc = sorted(indegree_centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_idc)
    ccdf = pd.DataFrame(sorted_idc,columns=["country","indegree_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # outdegree centrality
    # print("-" * 10, "outdegree centrality", "-" * 10)
    outdegree_centrality = nx.algorithms.centrality.out_degree_centrality(DG)
    sorted_odc = sorted(outdegree_centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_odc)
    ccdf = pd.DataFrame(sorted_odc,columns=["country","outdegree_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # closeness centrality indegree
    # print("-" * 10, "indegree closeness centrality", "-" * 10)
    closeness_centrality = nx.algorithms.centrality.closeness_centrality(DG)
    sorted_cc = sorted(closeness_centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_cc)
    
    ccdf = pd.DataFrame(sorted_cc,columns=["country","closeness_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # outdegree closeness centrality
    # print("-" * 10, "outdegree closeness centrality", "-" * 10)
    out_closeness_centrality = nx.algorithms.centrality.closeness_centrality(DG_out)
    sorted_cc_out = sorted(out_closeness_centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_cc_out)
    
    ccdf = pd.DataFrame(sorted_cc_out,columns=["country","out_closeness_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # betweenness centrality
    # print("-" * 10, "betweenness centrality", "-" * 10)
    betweenness_centrality = nx.algorithms.centrality.betweenness_centrality(DG, normalized=True, weight=True)
    sorted_bc = sorted(betweenness_centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_bc)
    
    ccdf = pd.DataFrame(sorted_bc,columns=["country","betweenness_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # eigenvector centrality
    # indegree
    # print("-" * 10, "indegree eigenvector centrality", "-" * 10)
    eigenvector_centrality = nx.eigenvector_centrality_numpy(DG, weight=True)
    sorted_ec = sorted(eigenvector_centrality.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_ec)
    
    ccdf = pd.DataFrame(sorted_ec,columns=["country","eigenvector_centrality"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # outdegree
    # print("-" * 10, "outdegree eigenvector centrality", "-" * 10)
    eigenvector_centrality_out = nx.eigenvector_centrality_numpy(DG_out, weight=True)
    sorted_ec_out = sorted(eigenvector_centrality_out.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_ec_out)
    
    ccdf = pd.DataFrame(sorted_ec_out,columns=["country","eigenvector_centrality_out"]).sort_values(["country"]).reset_index(drop=True)
    country_df = country_df.merge(ccdf, how="left", on="country")

    # network constraint
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

df_year_measures.shape

im = pd.read_csv("indices_merged.csv")
im.head()
im = im[['year','hdi_value', 'iso', 'hdi_rank', 'fgi_rank', 'fgi_value', 'hfi_rank', 'hfi_value']]
df_year_measures = df_year_measures.merge(im,on=["iso","year"],how="left")
df_year_measures.shape

wp = pd.read_csv("world_population_by_year.csv",skiprows=4)
wp = wp[["Country Code"]+list(map(str,range(2008,2018)))]
wp = wp.rename(columns={"Country Code":"iso"}).rename(columns=dict(zip(list(map(str,range(2008,2018))),list(range(2008,2018)))))
wp.head()

wp = pd.melt(wp, id_vars=["iso"], var_name="year", value_name="population")
wp[wp["iso"]=="ABW"]

df_year_measures['year'] = df_year_measures['year'].astype(int)
wp['year'] = wp['year'].astype(int)
df_year_measures['iso'] = df_year_measures['iso'].astype(str)
wp['iso'] = wp['iso'].astype(str)

df_year_measures = df_year_measures.merge(wp,on=["iso","year"],how="left")

df_year_measures.shape


msno.bar(df_year_measures)

df_year_measures.head()

df_year_measures.to_csv("country_year_features.csv",index=False)


