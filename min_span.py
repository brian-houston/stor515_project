import numpy as np
import pandas as pd
import networkx as nx


def minimum_spanning_tree(X, copy_X=True):
	"""X are edge weights of fully connected graph"""
	if copy_X:
		X = X.copy()
 
	if X.shape[0] != X.shape[1]:
		raise ValueError("X needs to be square matrix of edge weights")
	n_vertices = X.shape[0]
	spanning_edges = []
	 
	# initialize with node 0:
	visited_vertices = [0]
	num_visited = 1
    # exclude self connections:
	diag_indices = np.arange(n_vertices)
	X[diag_indices, diag_indices] = np.inf
     
	while num_visited != n_vertices:
		new_edge = np.argmin(X[visited_vertices], axis=None)
		# 2d encoding of new_edge from flat, get correct indices
		new_edge = divmod(new_edge, n_vertices)
		new_edge = [visited_vertices[new_edge[0]], new_edge[1]]
		# add edge to tree
		spanning_edges.append(new_edge)
		visited_vertices.append(new_edge[1])
		# remove all edges inside current tree
		X[visited_vertices, new_edge[1]] = np.inf
		X[new_edge[1], visited_vertices] = np.inf
		num_visited += 1
	return np.vstack(spanning_edges)


#Reading in/cleaning data
data = pd.read_csv('sandbox/combined_stock_data.csv', header=0, index_col=0)
data = data.drop(columns = ["KGNR", "FRMC"])
data = data.drop(["04-04-2022"])

#Running correlation/setting up graph
corr = data.corr()

corr_filter = nx.Graph()
for i in range(len(corr)-1):
	for j in range(i+1, len(corr)):
		if abs(corr.iloc[i,j]) > 0.6:
			corr_filter.add_edge(corr.columns.values[i], corr.columns.values[j])

#Running min span tree			
dist = np.sqrt(2*(1- corr))

dist = np.array(dist)
edge_list_raw = minimum_spanning_tree(dist)
edge_list = []
for i, j in edge_list_raw:
	edge = (corr.columns.values[i], corr.columns.values[j])
	edge_list.append(edge)

mst = nx.Graph()
for i, j in edge_list:
	mst.add_edge(i,j)

#Calculating peripheral edges
g = mst
d = nx.degree(g)
b_c = nx.betweenness_centrality(g)
c1 = max(d)

D_dg = {}
for n in g.nodes():
	D_dg[n] = nx.shortest_path_length(g, n, 'ZTS')

D_c = {}
sum_C = {}

for n in g.nodes():
	nbs = nx.neighbors(g, n)
	sum_C[n] = sum(corr[n][nb] for nb in nbs)
c2 = max(sum_C)

for n in g.nodes():
	D_c[n] = nx.shortest_path_length(g, n, c2)

D_d = {}
m_d = {}

for n in g.nodes():
	nodes = list(g.nodes())
	nodes.remove(n) 
	dd = [nx.shortest_path_length(g, n, ns) for ns in nodes]
	m_d[n] = np.mean(dd)
c3 = min(m_d)

for n in g.nodes():
	D_d[n] = nx.shortest_path_length(g, n, c3)


d = {node:val for (node, val) in g.degree()}
nodes_stats = pd.DataFrame.from_dict(d, orient='index')
nodes_stats.rename(columns={0:'Degree'}, inplace=True)
nodes_stats['Ddegree'] = D_dg.values()
nodes_stats['Dcorr'] = D_c.values()
nodes_stats['Ddis'] = D_d.values()
nodes_stats['Distance'] = (nodes_stats['Ddegree'] + nodes_stats['Dcorr'] + nodes_stats['Ddis'])/3
nodes_stats.head()

#Final peripheral portfolio
p = nodes_stats.sort_values(by='Distance', ascending = False).head(25)
portfolio_p = [name for name in p.index.values]
print(portfolio_p)
