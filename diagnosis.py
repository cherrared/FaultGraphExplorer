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
import modelingalgo as ma
import SMTF as sm



#####################################################################################################################
############################################# functions definition####################################################
#### define the global graph




#### define the dictionary of (node, value)
    
def vall(G):
 val={}
 for n in G.nodes():
    val[n]=True
 return(val)



#### Graph coloring
def color_graph(G, ObsF):
  color_map = []
  color_map2 = []
  for node in G.nodes():
      k=0
      print(node)
      while(k< len(ObsF) and node!= ObsF[k]):
        k=k+1
     
      if (k < len(ObsF)):
        color_map.append('red')
      elif (G.nodes[node]['n']==0 ):
        color_map.append('blue')
            
      elif (G.nodes[node]['n']==1 ):
        color_map.append('green')
              
      elif (G.nodes[node]['n']==2 ):
        color_map.append('orange')
              
      elif (G.nodes[node]['n']==3 ):
        color_map.append('pink')
      
  
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


##### Draw the graph
def dr_graph(G, color_map, color_map2):
  # write dot file to use with graphviz
  # run "dot -Tpng test.dot >test.png"
  write_dot(G,'test.dot')

  # same layout using matplotlib with no labels
  plt.title('dependency graph')
  pos =graphviz_layout(G, prog='dot')
  nx.draw(G,pos, with_labels= True,  edge_color= color_map2, node_color = color_map)


##### Extract the Sub-graph GG from G using the observations 

def graph_GG(G, nodes):
  print("***********************")
  print(nodes)
  neighbors=[]
  for i in nodes:
   neighbors.append(i)
   for j in list(G.neighbors(i)):
    neighbors.append(j)
    
   for j in list(G.predecessors(i)):
     neighbors.append(j)

   

  GG=G.subgraph(neighbors)
  
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
### non_shared_var between two services : a service is a list of nodes

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
   yaml.dump(data,topo)


def boucle_diag(G, ObsT, ObsF):
    


   
    Obs_total=[]

    ### color and draw the global graph
    color_map, color_map2=color_graph(G,ObsF)
    
    dr_graph(G, color_map, color_map2)
    
   


    plt.savefig("graph2.png")
    plt.show()





    ### get the sub-grah GG from obs in the list ObsF with the function GG_graph
    for i in ObsF:
     Obs_total.append(i)
    for i in ObsT:
     Obs_total.append(i)
    GF= graph_GG(G, Obs_total)
    
    ### color and draw the sub_graph
    for i in ObsF:
     Obs_total.append(i)
    for i in ObsT:
     Obs_total.append(i)
    color_map, color_map2=color_graph(GF,ObsF)
    
    dr_graph(GF, color_map, color_map2)
    



    plt.savefig("graph2.png")
    plt.show()
   

    
    
    ########## build the SMT file : Assertions
           
    fi = open("SMTF.py", "w")
    ## import:
      
    fi.write("from z3 import *")
    fi.write("\n")
   
    ### Functions
    # Define the function that returns the number of false values
    fi.write("def compte(m, liste):"+"\n")
    fi.write(" t=0"+"\n")
    fi.write(" for e in liste:"+"\n")
    fi.write("  if m[e]== False: t=t+1"+"\n")
    fi.write(" return(t)"+"\n")
    fi.write("def comp (s,m):"+"\n") 
    fi.write(" b=0"+"\n")
    fi.write(" for e in s:"+"\n")
    fi.write("  if str(s[e])== str(m) :"+"\n")
    fi.write("    b=b+1"+"\n")
    fi.write(" return b "+"\n")
 
       
    fi.write("def SMTAlgo(ObsT, ObsF): \n")
    ### Write the definition of variables in the SMT file:
    z=0
    for d in GF.nodes():
      if (z==0):
         fi.write(" "+str(d))
         z=z+1
      else: fi.write(","+str(d))
    fi.write(" =Bools('")
    z=0
    for d in GF.nodes():
     if (z==0):  
         fi.write(str(d))
         z=z+1
     else: 
        fi.write(" "+ str(d))
         
    fi.write("')") 
    fi.write("\n")

    #### write the assertions in the SMT file:
    
    fi.write(" s=Solver()")
    fi.write("\n")
    
    for node in GF.nodes():
      ne=[]
      z=0
      zz=0
      for i in GF.predecessors(node):
        ne.append(i)
      if len(ne)>1:
                 
         
        for  j in GF.predecessors(node):
          ## For "And" type dependencies:
         
          if ((GF[j][node]['at'] == 1) or (GF[j][node]['at'] == 2)):
            if (z==0):
          
              fi.write(" s.add("+str(node)+"==And("+str(j))
              z=z+1
            elif (z>0):
              fi.write(","+str(j))
               
           
           
          ## For "Or" type dependencies:
          
          if (GF[j][node]['at'] == 0):

            if ( zz==0 ):
              fi.write(" s.add("+str(node)+"==Or("+str(j))
              zz=zz+1
            elif (zz>0):
              fi.write(","+str(j))
            
        fi.write("))")
        fi.write("\n")          




              
     
    ## Delete the false observations and their succcessors from the list to keep only unknown variables
    FF= nx.DiGraph(GF)
    ll=[]
    for e in ObsF:
      ll=GF.successors(e)
    
      for m in ll:
        if m in ObsF == False:
          FF.remove_node(m)
    
     
        
    FF.remove_nodes_from(ObsF)
    FF.remove_nodes_from(ObsT)
   

    #### Add the observations:
    for i in ObsF:
      fi.write(" s.add("+ str(i) +"== False)")    
      fi.write("\n")   
    for i in ObsT:
      fi.write(" s.add("+ str(i) +"== True)")    
      fi.write("\n")  
    #### add the code for the result of SMT
     
    fi.write(" liste=[]\n")
    fi.write(" valT={}\n")
    fi.write(" valSF={}\n")
    for i in FF.nodes(): 
       fi.write(" liste.append("+str(i)+")\n")
       fi.write(" valT["+str(i)+"]="+str(FF.nodes[i]['T'])+"\n")
       fi.write(" valSF["+str(i)+"]="+str(FF.nodes[i]['SF'])+"\n")
   
    # Open the file of solutions
    fi.write(" fi = open(\"Solutions.txt\", \"w\")\n")  
    fi.write(" Sauve={}\n")
    fi.write(" Sauve2={}\n")
    fi.write(" save=[]\n")
   
    fi.write(" i=1\n")
    fi.write(" s.check() \n")
    fi.write(" c=compte(s.model(),liste)\n")
    fi.write(" Sauve[0]= (c,s.model())\n")
    fi.write(" Sauve2[0]= s.model()\n") 
    fi.write(" while s.check() == sat:")
    fi.write("\n")
    fi.write("  j=0\n")
    fi.write("  while j < len(liste):\n") 
    fi.write("   if ((s.check() == sat) and (comp(Sauve2, s.model())==0)): \n")
    fi.write("     c=compte(s.model(),liste)\n")   
    fi.write("     Sauve[i]= (c,s.model())\n")
    fi.write("     Sauve2[i]= s.model()\n")
    fi.write("     i=i+1\n")
    fi.write("   if (s.check()== sat): save= s.model()\n")
    fi.write("   if (save[liste[j]] == False):\n")
    fi.write("    s.add(And(liste[j] == True))\n")
    fi.write("   j=j+1\n")
    fi.write(" t=sorted(Sauve.itervalues())\n")
    fi.write(" i=0\n")
    fi.write(" while i<len(t):\n")
    fi.write("   Sauve[i]=t[i] \n")
    fi.write("   fi.write(str(i)+\":\"+str(t[i])+ \" \\n \")" +"\n")
    fi.write("   i=i+1\n")
    fi.write(" for e in liste:\n")
    fi.write("   if t[0][1][e] == False :\n") 
    # check if node e can be tested
    fi.write("     if valT[e] == 1 :\n") 
    # the node e can be teted
    
    fi.write("        print(\"Please check the value of: \", e) \n") 
    fi.write("        a=input() \n") 
    #fi.write("     while (a != True) and (a != False) :\n")
    #fi.write("      print(\"Please enter a False or True values\")\n")
    #fi.write("      a=input() \n")  
    # a= False 
    fi.write("        if a== False:\n") 
    #a= false, check the SF value
    fi.write("           if valSF[e]== 1: \n")
    fi.write("             print(e, \"  is the root cause\")\n")
    fi.write("             sys.exit(0)\n")
    fi.write("           elif valSF[e]==2: \n") 
    fi.write("             print(e, \"  is the root cause, check the auto recovery node\") \n")
    fi.write("             sys.exit(0)\n")
    # if a =true add it to extended node  file
    fi.write("           else:  ObsF.append(str(e)) \n") 
    #fi.write("print(\"************************ Adding the extended nodes to the file .....\") \n")
    # a= True extend the node e
    fi.write("        elif a== True: \n") 
    # if a = True add it to the added observation file
  
    fi.write("           ObsT.append(str(e)) \n")
    #fi.write("print(\"************************ Adding the true observations to the added obs  file .....\") \n")
    # if node e is not testable , extend the graph and add it to the extended observation file:
    fi.write("     elif valT[e] == 0:  \n")
    fi.write("       ObsF.append(str(e)) \n")
    fi.write(" return(ObsT, ObsF)")
  
    
   
    

    
  
     
    fi.close()
    #os.system('pwd')
    








if __name__ == "__main__":
   
     
    # Get the topology and the observations file 
    
    topo_path=sys.argv[1] # topology file path
    file_path=sys.argv[2] ## observation file path
    topo_path="./"+ str(topo_path)

    ## count the services
    cpt_service=1
    
    ## ObsF contains the observation variables
    
    ObsF=[]
    ObsT=[]

    #ObsT1=[]
    #ObsF1=[]

   
    G=nx.DiGraph()
      
    ## Read the obervation file and store it in data 
    
    filepath="./"+str(file_path)
    data=yaml_loader(filepath)
    l=data["Services"]
   

    ### Define the global graph without services  
    ### Call the modeling-algo 

    G= ma.dependency_graph(topo_path)


    ### Add the service part and observations
    ### Fill the ObsF of the list for red: False services "without the register services"
    ll=l
    lll=l
    l=l["False_values"]
    if l != None:
     v=0
     while v< len(l) :
      
      service_obs= l[v]

      if  ("Register" in service_obs) == False:
        
        ObsF.append(service_obs)
      v=v+1
    
    

     ### Define the graph for Register with red value:
    
     cpt_service=1 # number of register services identified
     v=0
     while v < len(l) :
      
      service_obs= l[v]
      if  ("Register" in service_obs) == True:
        RS= l[v] # Get the register services list 
       
        t=0 # Get each element of the Register list
        Register_Services=[]
        while t < len(RS["Register"]):
          Register_Services.append(str(RS["Register"][t]))
          t=t+1
        

        ## Construct the service graph element  
        ## cpt_register gets the number of registers in the dependency graph sharing the same variables

        cpt_register= md.Service_Register_modeling(G,topo_path,Register_Services, cpt_service)

        ## get the value of the number of affected register services
        i=1

        while i<= cpt_register :
         
         ObsF.append("Register{0}{1}".format(cpt_service, i))
         i=i+1 

             
          
      
        cpt_service=cpt_service+1

       


          
      
      
      v=v+1



    ## Get the "True" values:
    ll=ll["True_values"]
   
    if (ll != None):
      v=0
      
      while v< len(ll) :
        
        service_obs= ll[v]

        if  ("Register" in service_obs) == False:
          
          ObsT.append(service_obs)
        v=v+1
    
    


      ### Define the graph for Register with a "True" value:
      
      
      v=0
      while v < len(ll) :
        
        service_obs= ll[v]
        if  ("Register" in service_obs) == True:
          RS= ll[v] # Get the register services list 
        
          t=0 # Get each element of the Register list
          Register_Services=[]
          while t < len(RS["Register"]):
            Register_Services.append(str(RS["Register"][t]))
            t=t+1
          

          ## Construct the service graph element  
          ## cpt_register gets the number of registers in the dependency graph sharing the same variables

          cpt_register= md.Service_Register_modeling(G,topo_path,Register_Services, cpt_service)

          ## get the value of the number of affected register services
          i=1

          while i<= cpt_register :
          
            ObsT.append("Register{0}{1}".format(cpt_service, i))
            i=i+1 

              
            
        
          cpt_service=cpt_service+1

        


            
        
        
        v=v+1
  








    # Affect false values for False observations:
    val=vall(G)
    for i in ObsF:
      val[i]= False
    # Affect True values for True Observations:
    
    for i in ObsT:
      val[i]= True
   
 
    while True:
    
     #Create the SMT file with the current observations
     boucle_diag(G, ObsT, ObsF)    
     
     # reload the SMT file 
     reload(sm)
     # execute the SMT file 
     ObsT, ObSF= sm.SMTAlgo(ObsT, ObsF)
    
  