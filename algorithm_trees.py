#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Debbie Wagenaar
# Created Date: April 2021
# =============================================================================
""" 
This code determines the minimum amount of tiles and bond-edge types needed in
scenario 2 and/or 3 for tile-based DNA-assembly and draws the trees coming out 
of the algorithm. The algorithms programmed are described in "Minimal tile and 
bond-edge types for self-assembling DNA graphs" by J. Ellis-Monaghan et. al. 

To use this code you need to create a graph G (see example below)
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
G.add_edges_from([(1,2),(2,3),(2,5),(5,6),(3,4),(3,7),(7,8),(8,9),(8,10)])

and next call the desired algorithm (scenario 2 or 3)
"""
# =============================================================================
# Imports
# =============================================================================

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

#Make an LSO of a graph G
def LSO(G):
    #Make empty directed graph
    T = nx.DiGraph()
    T.add_nodes_from(list(G.nodes))
    
    #Make LSO
    for u,v,a in list(G.edges(data=True)):
        G.remove_edge(u, v)
        l1 = len(nx.node_connected_component(G,u))
        l2 = len(nx.node_connected_component(G,v))
        if l2>l1:
            T.add_edge(v,u)
        else:
            T.add_edge(u,v)
        G.add_edge(u,v)
            
    #Draw LSO
    pos = graphviz_layout(T, prog="dot")
    nx.draw(T, pos, with_labels=True)
    plt.savefig("LSO.png") # save as png
    plt.show() # display
    return T

#Scenario 2
def alg2(G):
    #Make an LSO of graph G
    T = LSO(G)
    
    #Find the root
    root = 0
    for n,d in T.in_degree():
        if d == 0:
            root = n
    
    #Traverse through the tree from the leaves to the root
    T_list = list(nx.dfs_postorder_nodes(T, source = root))

    labels = []
    tiles = []
    
    #Label all the edges
    for x in T_list:
        if x != root: 
            k = len(list(nx.dfs_tree(T, x))) #Determine size of subtrees
            T.edges[list(T.predecessors(x))[0], x]["labels"] = k #Label the edge with size of subtree
            if k not in labels: #Add label to list of labels for total
                labels.append(k)
        tile = []
        if list(T.successors(x)) == []: #Add first empty tile for leaves
            if tile not in tiles:
                tiles.append([])
        else:
            #Determine lesser-subtree sequence
            for i in list(nx.dfs_preorder_nodes(T, source = x)): 
                tile.append(len(list(nx.dfs_tree(T, i))))
            tile.sort()
            if tile not in tiles: #Add new tiles for total
                tiles.append(tile)
    
    #Draw LSO with bond-edge types
    pos = graphviz_layout(T, prog="dot")
    nx.draw(T, pos, with_labels=True)
    nx.draw_networkx_edge_labels(T, pos, edge_labels=nx.get_edge_attributes(T,'labels'), font_color='green')
    plt.savefig("scenario2.png") 
    plt.show() 
    
    return(len(labels), len(tiles))

#scenario 3
def alg3(G):
    #Make an LSO of graph G
    T = LSO(G)
    
    #Determine the height
    h = nx.dag_longest_path_length(T)
    
    #Find the root
    root = 0
    for n,d in T.in_degree():
        if d == 0:
            root = n  

    subgraphs = []
        
    #Find the leaves and labelling those edges with 1
    for x in T.nodes():
        if T.out_degree(x) == 0 and T.in_degree(x) == 1:
            T.edges[list(T.predecessors(x))[0], x]["labels"] = 1
    
    j = 1
    for i in range(h-1, 0, -1): #Iterate over the levels from bottom to top
        for l in list(nx.descendants_at_distance(T,root,i)): #Iterate over vertices per level
            if subgraphs == []:
                if T.edges[list(T.predecessors(l))[0], l] == {}:
                    j = j + 1
                    T.edges[list(T.predecessors(l))[0], l]["labels"] = j #Label the edges
                subgraphs.append(nx.dfs_tree(T,l)) #Add current subtree to list
            else:
                if not any([nx.is_isomorphic(nx.dfs_tree(T,l), sub) for sub in subgraphs]) and T.edges[list(T.predecessors(l))[0], l] == {}:
                    j = j + 1
                    T.edges[list(T.predecessors(l))[0], l]["labels"] = j
                subgraphs.append(nx.dfs_tree(T,l)) #Add current subtree to list
    
    #Draw LSO with bond-edge types
    pos = graphviz_layout(T, prog="dot")
    nx.draw(T, pos, with_labels=True)
    nx.draw_networkx_edge_labels(T, pos, edge_labels=nx.get_edge_attributes(T,'labels'), font_color='green')
    plt.savefig("scenario3.png") 
    plt.show()
    return(j, j+1)

#Make a graph
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7,8,9])
G.add_edges_from([(1,3),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(6,9)])

nx.draw(G, with_labels=True)
plt.savefig("G.png") # save as png
plt.show()

b2,t2 = alg2(G)
print("B2 =", b2, "and T2 =", t2)

b3,t3 = alg3(G)
print("B3 =", b3, "and T3 =", t3)
