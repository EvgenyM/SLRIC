from methods.indirect_influence import indirect_pagerank, indirect_paths
from methods.direct_influence import pairwise_inf
from classes.GraphQW import GraphQW, nx


""" LRIC centrality
Arguments:
graph - input graph (Graph or DiGraph object, NetworkX package)
q (optional) - quota (threshold of influence) for each node (share of weighted in-degree). By default q = 20%
dq (optional) - predefined fixed threshold value for each node (float, array or dictionary)
group_size (optional) - maximal group size (cardinality of coalition). By default limcoal = 4
dw (optional) - nodes size (float, array or dictionary). By default node size is equal to weighted out-degree.
group_size (optional) - maximal length of influence
models (optional) - type of LRIC centrality (LRIC_max, LRIC_maxmin, LRIC_pagerank). By default models = "max"
data - logical scalar. If the data arguments is False, then nodes centrality is returned. 
Otherwise, centrality and SRIC graph is returned. By default data = false

Output:
ranking - nodes SRIC centrality (dictionary)
g - SRIC graph
"""
def lric(graph, q=20, dq=None, group_size=4, dw=None, limpath=3, models='max', data=False):
    if isinstance(models, str):
        models = [models]
    g = pairwise_inf(GraphQW(graph, q, dq, group_size, dw), method='LRIC')  # evaluate direct influence
    if 'pagerank' in models:  # calculate LRIC PageRank
        ranking = indirect_pagerank(g).aggregate()
        g.set_param('lric_pagerank', ranking)
    if 'max' in models:  # calculate LRIC_Max
        ranking = indirect_paths(g, limpath, 0, 2).aggregate()
        g.set_param('lric_max', ranking)
    if 'maxmin' in models:
        ranking = indirect_paths(g, limpath, 0, 1).aggregate()
        g.set_param('lric_maxmin', ranking)
    if data:
        return ranking, g
    else:
        return ranking


""" SRIC centrality
Arguments:
graph - input graph (Graph or DiGraph object, NetworkX package)
q (optional) - quota (threshold of influence) for each node (share of weighted in-degree). By default q = 20%
dq (optional) - predefined fixed threshold value for each node (float, array or dictionary)
group_size (optional) - maximal group size (cardinality of coalition). By default limcoal = 4
dw (optional) - nodes size (float, array or dictionary). By default node size is equal to weighted out-degree.
data - logical scalar. If the data arguments is False, then nodes centrality is returned. 
Otherwise, centrality and SRIC graph is returned. By default data = false

Output:
ranking - nodes SRIC centrality (dictionary)
g - SRIC graph
"""


def sric(graph, q=20, dq=None, group_size=4, dw=None, dCoal=None, data=False):
    g = pairwise_inf(GraphQW(graph, q, dq, group_size, dw), method='SRIC') # calculate SRIC graph
    ranking = g.aggregate(name='sric') # calculate centrality of each node
    if data:
        return ranking, g
    else:
        return ranking
