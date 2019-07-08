#!/usr/bin/env python3

from z3 import *
import pygraphviz
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
#import pylab as plt
from matplotlib import interactive
import sys
from scipy import *
import os
import subprocess
import networkx as nx
import modeling as md
import yaml


#####################################################################################################################
############################################# functions definition####################################################
#### define the global graph
### list to match between the nodes id and their name


#### affect values to nodes

def affect(G,node,val):
  val[node]=False

#### define the dictionary of (node, value)
    
def vall(G):
 val={}
 for n in G.nodes():
   
   #print(n)
   val[n]=True
 return(val)



#### color the graph
def color_graph(G, lignes):
  color_map = []
  color_map2 = []
  #print(G.nodes["s"]['AG'])
  for node in G.nodes():
      k=0
      print(node)
      while(k< len(lignes) and node!= lignes[k]):
        k=k+1
     
      if (k < len(lignes)):
        color_map.append('red')
      elif (G.nodes[node]['n']==0 ):
        color_map.append('blue')
            
      elif (G.nodes[node]['n']==1 ):
        color_map.append('green')
              
      elif (G.nodes[node]['n']==2 ):
        color_map.append('orange')
              
      elif (G.nodes[node]['n']==3 ):
        color_map.append('pink')
      elif (G.nodes[node]['n']==4 ):
        color_map.append('grey')
  
  #print(G.edges())
  #"print(G['s1']['s']['at'])
  for e in G.edges():
    if (G[e[0]][e[1]]['at']==0):
      color_map2.append('green')
    if (G[e[0]][e[1]]['at']==1):
      color_map2.append('blue')
    if (G[e[0]][e[1]]['at']==2):
      color_map2.append('orange')
    if (G[e[0]][e[1]]['at']==3):
      color_map2.append('pink')
  return(color_map, color_map2)
##### draw the graph
def dr_graph(G, color_map, color_map2):
  # write dot file to use with graphviz
  # run "dot -Tpng test.dot >test.png"
  write_dot(G,'test.dot')

  # same layout using matplotlib with no labels
  plt.title('dependency graph')
  pos =graphviz_layout(G, prog='dot')


  nx.draw(G,pos, with_labels= True,  edge_color= color_map2, node_color = color_map)

##### graph extraction
def graph_GG(G, nodes):
  #print(nodes)
  neighbors=[]
  for i in nodes:
   neighbors.append(i)
   for j in list(G.neighbors(i)):
    neighbors.append(j)
    
   for j in list(G.predecessors(i)):
    if (G.nodes[j]['n']==4):
      for l in list(G.predecessors(j)):
        neighbors.append(l)

    neighbors.append(j)

   
  #print(neighbors)

  GG=G.subgraph(neighbors)
  """ for i in nodes:
  GG.add_nodes_from(G.neighbors(i))
  GG"""
  return(GG)
######## Function of shared variables with services #####################

def shared_var(G, service,service2):

  neighbors=[]
  
  #print(neighbors[0])
  for j in list(G.neighbors(service)):
    neighbors.append(j)
  for j in list(G.predecessors(service)):
    neighbors.append(j)
 
  
 
   
  neighbors1=[]
  for j in list(G.neighbors(service2)):
        neighbors1.append(j)
  for j in list(G.predecessors(service2)):
        neighbors1.append(j)
  shar=[]
  n=0      ### for the case where there is no shared var                                  
  for f in neighbors:
      
    
    j=0
    k=0
    while (k<len(neighbors1)) and (f != neighbors1[j]):
              j=j+1
              k=k+1
        
    if k<len(neighbors1):
        n=n+1   #number of shared var 
        shar.append(f)
  
  

  return(shar,n)
### non_shared_var Function

def non_shared_var(G, service1, service2):
    l,n = shared_var(G,service1,service2)
    neighbors=[] 
    for j in list(G.neighbors(service1)):
      neighbors.append(j)
    for j in list(G.predecessors(service2)):
      neighbors.append(j) 
     
    for i in l:
      
      neighbors.remove(i)
    return(neighbors)
def yaml_loader(filepath):
  with open(filepath, "r") as topo:
      data = yaml.load(topo)
  return data
def yaml_dump(filepath, data):
   yaml.dump(data, topo)

def dependency_graph(topofile):

   
   
    topo_path="./"+ str(topofile)
  
    
    G=nx.DiGraph()
    
    
    ### define the global graph without services  
    G= md.global_graph(topo_path)


   
    return G


if __name__ == "__main__":
  
      # to excute directly the modeling algo
      topofile=sys.argv[1]
      G=dependency_graph(topofile)
      ### define the dictionary of boolean values
      lignes=[]
      val=vall(G)
      ### affect the false values 
      
    
      
  
      ### color and draw the global graph
      color_map, color_map2=color_graph(G,lignes)
    
      dr_graph(G, color_map, color_map2)
    



      plt.savefig("graph2.png")
      plt.show()