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
import subprocess
import threading

#####################################################################################################################
############################################# functions definition####################################################

#### define the global graph

#### define the dictionary of (node, value)


def vall(G):
    val = {}
    for n in G.nodes():
        val[n] = True
    return (val)


#### Graph coloring
def color_graph(G, ObsF, ObsT, ObsN):
    color_map = []
    color_map2 = []

    for node in G.nodes():
        k = 0
<<<<<<< HEAD
        print("hhhhhhhhhhhhhhhhhhh")
        print(node)
        for element in ObsF:
            if str(node) == str(element):
                color_map.append('red')
                k = k + 1

        # if the node is in ObsF tnan:
        for element in ObsT:
            if str(node) == str(element):
                color_map.append('green')
                k = k + 1
        for element in ObsN:
            if str(node) == str(element):
                print("hhhhhhhhhh")
                print(element + "===" + node)
                color_map.append('orange')
                k = k + 1
        if (G.nodes[node]['n'] == 0 and k < 1):
            color_map.append('blue')

        elif (G.nodes[node]['n'] == 1 and k < 1):
            color_map.append('gray')

        elif (G.nodes[node]['n'] == 2 and k < 1):
=======

        while (k < len(ObsF) and node != ObsF[k]):
            k = k + 1
        # if the node is in ObsF tnan:
        if (k < len(ObsF)):
            color_map.append('red')
        if node in ObsT:
            color_map.append('green')
        if node in ObsN:
            color_map.append('orange')

        elif (G.nodes[node]['n'] == 0):
            color_map.append('blue')

        elif (G.nodes[node]['n'] == 1):
            color_map.append('gray')

        elif (G.nodes[node]['n'] == 2):
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
            color_map.append('yellow')

        elif (G.nodes[node]['n'] == 3 and k < 1):
            color_map.append('pink')

    for e in G.edges():
        if (G[e[0]][e[1]]['at'] == 0):
            color_map2.append('green')
        if (G[e[0]][e[1]]['at'] == 1):

            color_map2.append('blue')
        if (G[e[0]][e[1]]['at'] == 2):

            color_map2.append('orange')
        if (G[e[0]][e[1]]['at'] == 3):
            color_map2.append('pink')

    return (color_map, color_map2)


## node position definition
def pos_def(G):

    pos_0x = 0
    pos_1x = 0
    pos_2x = 0
    pos_3x = 0
    pos = {}
    for node in G.nodes():

        if (G.nodes[node]['n'] == 0):

            pos[node] = (pos_0x, 18.0)
            pos_0x = pos_0x + 100

        elif (G.nodes[node]['n'] == 1):

            pos[node] = (pos_1x, 90.0)
            pos_1x = pos_1x + 10000.0
        elif (G.nodes[node]['n'] == 2):

            pos[node] = (int(pos_2x), 162.0)
            pos_2x = pos_2x + 10000.0
        elif (G.nodes[node]['n'] == 3):

            pos[node] = (int(pos_3x), 200)
            pos_3x = pos_3x + 10000.0

    return (pos)


##### Draw the graph
def dr_graph(G, i, ax, color_map, color_map2, pos):
    # write dot file to use with graphviz
    # run "dot -Tpng test.dot >test.png"
    write_dot(G, 'test.dot')

    # same layout using matplotlib with no labels

<<<<<<< HEAD
    #ax[i].set_axis_off()
    #if i == 0:
    #    ax[i].set_title('Global Dependency Graph')
    #else:
    #    ax[i].set_title('Dependency sub_graph')
=======
    ax[i].set_axis_off()
    if i == 0:
        ax[i].set_title('Global Dependency Graph')
    else:
        ax[i].set_title('Dependency sub_graph')
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    ### draw with random positions : if not comment the following
    pos = graphviz_layout(G, prog='dot')

    nx.draw(G,
            pos,
            ax=ax[i],
            with_labels=True,
            edge_color=color_map2,
            node_color=color_map)


##### Extract the Sub-graph GG from G using the observations


<<<<<<< HEAD
def graph_GG(G, ObsF, nodes):
=======
def graph_GG(G, nodes):
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978

    neighbors = []
    for i in nodes:
        neighbors.append(i)
    # for j in list(G.neighbors(i)):
    #        neighbors.append(j)

    for j in ObsF:
        for node in list(G.predecessors(j)):
            neighbors.append(node)

    GG = G.subgraph(neighbors)

    return (GG)


def yaml_loader(filepath):
    with open(filepath, "r") as topo:
        data = yaml.load(topo)
    return data


def yaml_dump(filepath, data):
    yaml.dump(data, topo)


def draw_global_graph(G, ObsT, ObsF, ObsN):
    ### color and draw the global graph
    color_map, color_map2 = color_graph(G, ObsF, ObsT, ObsN)
<<<<<<< HEAD
    #fig, axes = plt.subplots(nrows=1, ncols=2)
    #ax = axes.flatten()
    pos = pos_def(G)
    ax = {}
=======
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()
    pos = pos_def(G)
    os.system('')
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    dr_graph(G, 0, ax, color_map, color_map2, pos)

    # split the image into 2 axes

    #plt.savefig("graph2.png")
<<<<<<< HEAD
    plt.show()
=======
    #plt.show()
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978


def draw_subgraph(G, ObsT, ObsF, ObsN):

    Obs_total = []
    pos = pos_def(G)
    ax = {}
    ### get the sub-grah GG from obs in the list ObsF with the function GG_graph
    print(
        "**********************************************************************"
    )
    print('False observations: Nodes down:')
    for i in ObsF:
        Obs_total.append(i)
        print(i)
    print(
        "**********************************************************************"
    )
    print('True observations: Nodes Up:')
    for i in ObsT:
        Obs_total.append(i)
<<<<<<< HEAD
        print(i)
    print(
        "**********************************************************************"
    )
    print('Suspect Nodes:')
    for i in ObsN:
        Obs_total.append(i)
    GF = graph_GG(G, ObsF, Obs_total)

    ### color and draw the sub_graph

    color_map, color_map2 = color_graph(GF, ObsF, ObsT, ObsN)
    pos = pos_def(G)
    print(
        "**********************************************************************"
    )
    print(" Creating the sub_graph...")
    dr_graph(GF, 1, ax, color_map, color_map2, pos)

    #plt.savefig("graph3.png")
    plt.show()
    return (GF)

=======

    GF = graph_GG(G, Obs_total)

    ### color and draw the sub_graph
    for i in ObsF:
        Obs_total.append(i)
    for i in ObsT:
        Obs_total.append(i)
    for i in ObsN:
        Obs_total.append(i)
    color_map, color_map2 = color_graph(GF, ObsF, ObsT, ObsN)
    pos = pos_def(G)
    dr_graph(GF, 1, ax, color_map, color_map2, pos)

    #plt.savefig("graph3.png")
    plt.show()
    ########## build the SMT file : Assertions
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978

def boucle_diag(G, ObsT, ObsF, ObsN):

    draw_global_graph(G, ObsT, ObsF, ObsN)
    GF = draw_subgraph(G, ObsT, ObsF, ObsN)

    ########## build the SMT file : Assertions
    print(
        "**********************************************************************"
    )
    print(" Creating the SMT_file...")
    fi = open("SMTF.py", "w")
    ## import:

    fi.write("from z3 import *")
    fi.write("\n")

    ### Functions
    # Define the function that returns the number of false values
    fi.write("def compte(m, liste):" + "\n")
    fi.write(" t=0" + "\n")
    fi.write(" for e in liste:" + "\n")
    fi.write("  if m[e]== False: t=t+1" + "\n")
    fi.write(" return(t)" + "\n")
    fi.write("def comp (s,m):" + "\n")
    fi.write(" b=0" + "\n")
    fi.write(" for e in s:" + "\n")
    fi.write("  if str(s[e])== str(m) :" + "\n")
    fi.write("    b=b+1" + "\n")
    fi.write(" return b " + "\n")

<<<<<<< HEAD
    fi.write("def SMTAlgo(ObsT, ObsF, ObsN, extend, stop): \n")
=======
    fi.write("def SMTAlgo(ObsT, ObsF, ObsN, extend): \n")
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    ### Write the definition of variables in the SMT file:
    z = 0
    for d in GF.nodes():
        if (z == 0):
            fi.write(" " + str(d))
            z = z + 1
        else:
            fi.write("," + str(d))
    fi.write(" =Bools('")
    z = 0
    for d in GF.nodes():
        if (z == 0):
            fi.write(str(d))
            z = z + 1
        else:
            fi.write(" " + str(d))

    fi.write("')")
    fi.write("\n")

    #### write the assertions in the SMT file:

    fi.write(" s=Solver()")
    fi.write("\n")

    dico_pred = {}
    for node in GF.nodes():
        num_predecessors = 0
        ne = []
        z = 0
        zz = 0
        for i in GF.predecessors(node):
            ne.append(i)
            num_predecessors = num_predecessors + 1
        # affect the number of predecessors of each node
        dico_pred[node] = num_predecessors
        if len(ne) > 1:

            for j in GF.predecessors(node):
                ## For "And" type dependencies:

                if ((GF[j][node]['at'] == 1) or (GF[j][node]['at'] == 2)):
                    if (z == 0):

                        fi.write(" s.add(" + str(node) + "==And(" + str(j))
                        z = z + 1
                    elif (z > 0):
                        fi.write("," + str(j))

                ## For "Or" type dependencies:

                if (GF[j][node]['at'] == 0):

                    if (zz == 0):
                        fi.write(" s.add(" + str(node) + "==Or(" + str(j))
                        zz = zz + 1
                    elif (zz > 0):
                        fi.write("," + str(j))

            fi.write("))")
            fi.write("\n")

    ## Delete the false observations and their succcessors from the list to keep only unknown variables
    FF = nx.DiGraph(GF)
    ll = []
    for e in ObsF:
        ll = GF.successors(e)

        for m in ll:
            if m in ObsF == False:
                FF.remove_node(m)

    FF.remove_nodes_from(ObsF)
    FF.remove_nodes_from(ObsT)
    FF.remove_nodes_from(ObsN)

    #### Add the observations:
    for i in ObsF:
        fi.write(" s.add(" + str(i) + "== False)")
        fi.write("\n")
    for i in ObsT:
        fi.write(" s.add(" + str(i) + "== True)")
        fi.write("\n")
    for i in ObsN:
<<<<<<< HEAD
        fi.write(" s.add(" + str(i) + "== True)")
=======
        fi.write(" s.add(" + str(i) + "== None)")
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
        fi.write("\n")
    #### add the code for the result of SMT

    fi.write(" liste=[]\n")

    fi.write(" valT={}\n")
    fi.write(" valSF={}\n")

    fi.write(" num_pred={}\n")
    for i in FF.nodes():
        fi.write(" liste.append(" + str(i) + ")\n")
        fi.write(" valT[" + str(i) + "]=" + str(FF.nodes[i]['T']) + "\n")
        fi.write(" valSF[" + str(i) + "]=" + str(FF.nodes[i]['SF']) + "\n")
        fi.write(" num_pred[" + str(i) + "]=" + str(dico_pred[i]) + "\n")

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
    fi.write("   fi.write(str(i)+\":\"+str(t[i])+ \" \\n \")" + "\n")
    fi.write("   i=i+1\n")
    # look for the false solutions that are not in the known observations, "liste" contains only unknown observations
    fi.write(" for e in liste:\n")
    fi.write("   if t[0][1][e] == False :\n")
    # check if node e can be tested
    fi.write("     if valT[e] == 1 :\n")
    # the node e can be tested

    fi.write("        print(\"Please check the value of: \", e) \n")
    fi.write("        a=input() \n")
    #fi.write("     while (a != True) and (a != False) :\n")
    #fi.write("      print(\"Please enter a False or True values\")\n")
    #fi.write("      a=input() \n")
    # a= False
    fi.write("        if a== False:\n")
    #a= false, check the SF value
    # if SF=1 then SF is true
    fi.write("           if valSF[e]== 1: \n")
    # if the node has no predecessors so the node is the RC:
<<<<<<< HEAD
    fi.write("            if num_pred[e]== 0: \n")
    fi.write("             print(e, \"  is the root cause\")\n")
    fi.write("             stop= True\n")
    fi.write("             ObsF.append(str(e))\n")
=======
    fi.write("            if num_pred[i]== 0: \n")
    fi.write("             print(e, \"  is the root cause\")\n")
    fi.write("             sys.exit(0)\n")
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    # if the node has predecessors it could be the root cause
    fi.write("            else:\n")
    fi.write("             print(e, \"  Possible root cause? Yes/No\")\n")
    fi.write("             answer= input()\n")
    fi.write("             if answer==\"Yes\": \n")
    fi.write("               print(e, \"  is the root cause\")\n")
<<<<<<< HEAD
    fi.write("               stop= True\n")
    fi.write("               ObsF.append(str(e))\n")
=======
    fi.write("               sys.exit(0)\n")
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    fi.write("             else:  ObsF.append(str(e)) \n")
    # if node is SF with auto-recovery
    fi.write("           elif valSF[e]==2: \n")
    # with no predecessors:
<<<<<<< HEAD
    fi.write("            if num_pred[e]== 0: \n")
    fi.write("             print(e, \"  is the root cause\")\n")
    fi.write("             stop=True\n")
    fi.write("             ObsF.append(str(e))\n")
    fi.write("            else:\n")
    # with predecessors
    fi.write(
        "             print(e, \"  Possible root cause with auto_recovery node? Yes/No\")\n"
    )
    fi.write("             answer= input()\n")
    fi.write("             if answer==\"Yes\": \n")
    fi.write(
        "               print(e, \"  is the root cause , check the auto recovery node\")\n"
    )
    fi.write("               stop=True\n")
    fi.write("               ObsF.append(str(e))\n")
=======
    fi.write("            if num_pred[i]== 0: \n")
    fi.write("             print(e, \"  is the root cause\")\n")
    fi.write("             sys.exit(0)\n")
    fi.write("            else:\n")
    # with predecessors
    fi.write(
        "             print(e, \"  Possible root cause with auto_recovery node? Yes/No\")\n"
    )
    fi.write("             answer= input()\n")
    fi.write("             if answer==\"Yes\": \n")
    fi.write(
        "               print(e, \"  is the root cause , check the auto recovery node\")\n"
    )
    fi.write("               sys.exit(0)\n")
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    fi.write("           else:  ObsF.append(str(e)) \n")
    # a= True extend the node e
    fi.write("        elif a== True: \n")
    # if a = True add it to the added observation file

    fi.write("           ObsT.append(str(e)) \n")
    # next solution
    fi.write("           extend= False \n")
    # if the test is unavailable
    fi.write("        elif a== None:  \n")
    # next solution
    fi.write("             ObsN.append(str(e)) \n")
    fi.write("             extend= False \n")

    fi.write("     elif valT[e] == 0:  \n")
    fi.write("       ObsN.append(str(e)) \n")
    #next solution
    fi.write("       extend= False \n")
<<<<<<< HEAD
    fi.write(" return(ObsT, ObsF, ObsN, liste, extend, stop)")
=======
    fi.write(" return(ObsT, ObsF, ObsN, liste, extend)")
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978

    fi.close()


if __name__ == "__main__":

    # Get the topology and the observations file
    print(
        "**********************************************************************"
    )
    print(" Reading the topology and the observations files...")
    topo_path = sys.argv[1]  # topology file path
    file_path = sys.argv[2]  ## observation file path
    topo_path = "./" + str(topo_path)

    ## count the services
    cpt_service = 1

    ## ObsF contains the False observation variables

    ObsF = []
    ObsT = []
    ObsN = []
    extend = True
<<<<<<< HEAD
    stop = False
    print(
        "**********************************************************************"
    )
    print(" Creating the global dependency graph...")
=======

>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
    G = nx.DiGraph()

    ## Read the obervation file and store it in data

    filepath = "./" + str(file_path)
    data = yaml_loader(filepath)
    l = data["Services"]

    ### Define the global graph without services
    ### Call the modeling-algo

    G = ma.dependency_graph(topo_path)

    ### Add the service part and observations
    ### Fill the ObsF of the list for red: False services "without the register services"
    ll = l
    lll = l
    l = l["False_values"]
    if l != None:
        v = 0
        while v < len(l):

            service_obs = l[v]

            ObsF.append(service_obs)
            v = v + 1

    ## Get the "True" values:
    ll = ll["True_values"]

    if (ll != None):
        v = 0

        while v < len(ll):

            service_obs = ll[v]

            ObsT.append(service_obs)
            v = v + 1

    # Affect false values for False observations:
    val = vall(G)
    for i in ObsF:
        val[i] = False
    # Affect True values for True Observations:

    for i in ObsT:
        val[i] = True
    # Affect None values for Suspect Observations:

    for i in ObsN:
        val[i] = None

    message = 0
    liste_diff = []
    liste_smt = []
    x = 0

    while message == 0 and stop == False:

        #Create the SMT file with the current observations
        boucle_diag(G, ObsT, ObsF, ObsN)

        # reload the SMT file
        reload(sm)
        # execute the SMT file
<<<<<<< HEAD
        ObsT, ObSF, ObsN, liste_smt, extend, stop = sm.SMTAlgo(
            ObsT, ObsF, ObsN, extend, stop)
=======
        ObsT, ObSF, ObsN, liste_smt, extend = sm.SMTAlgo(
            ObsT, ObsF, ObsN, extend)
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
        ## check if we have same solutions
        if x > 0:
            if liste_diff == liste_smt:
                message = 1
        liste_diff = liste_smt
        x = x + 1

    if message == 1:
        print("More observations are needed !!")
<<<<<<< HEAD
    draw_subgraph(G, ObsT, ObsF, ObsN)
=======
>>>>>>> 62fef6127916f0f2e4109ce0e670f8e87879a978
