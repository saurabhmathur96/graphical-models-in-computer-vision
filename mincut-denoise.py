from PIL import Image

import networkx as nx
import numpy as np

alpha, beta = 2, 1
X = np.array(Image.open('snoisy.png').convert('1'))
width, height = X.shape
G = nx.grid_2d_graph(width, height)

#
# pairwise

# sideways
for i in range(0, width):
	for j in range(0, height-1):
		G[(i,j)][(i,j+1)]['weight'] = beta*(X[i,j] != X[i,j+1])


# up-down
for i in range(0, width-1):
	for j in range(0, height):
		G[(i,j)][(i+1,j)]['weight'] = beta*(X[i,j] != X[i+1,j])


#
# unary

for i in range(0, width):
    for j in range(0, height):
        G.add_edge('s', (i,j), weight=alpha * X[i, j] )
        G.add_edge('t', (i,j), weight=alpha * (1-X[i, j]))

(cost, (set1, set2)) = nx.minimum_cut(G, 's', 't', capacity='weight')
if('s' not in set1):
	(set2, set1) = (set1, set2)

Y = np.zeros_like(X)
for i in range(width):
	for j in range(height):
		Y[i,j] = int((i,j) in set1)

Image.fromarray(Y).save('sdenoised.png')
