#!/usr/bin/env python3

import sys
import os
import networkx as nx


#************************## definitions########################################
############################ Nodes attributes ############################""
#SF: spontaneous faults, 0 : non SF and 1 for SF node , SF=2 spontaneous fault with auto recovery
#n=0 --> physrical layer , n=1 --> virtual layer, n=2 --> Application layer, n=3 --> service layer
# T : a testable node or no : if T=1 -->testable , if T=0 --> non Testable
#at=0--> or, at= 1--> and, at=2--> function (not a--> not b), at=3 --> function (a-->b)
# ClusterS--> for docker status, ClusterC--> for docker connection , clusterA--> for application elasticity, ClusterD--> for docker elasticity
#"""*********************************************
#*********************************************"""
#*************************###### physical env: n=0
def Sites(G, nb):
    # define the coarse node s englobing all the sites
    # n=0 (physical)

    G.add_node("s", SF=0, n=0, T=0)
    # Node s_i for each site i
    i = 1
    while i <= nb:
        G.add_node("s%i" % i, SF=1, n=0, T=1)
        G.add_edges_from([("s%i" % i, "s")], at=1)
        i = i + 1
    # The dependencies between sites


# The physical connection between sites
def PCon_Sites(G, i, j):
    G.add_node("c{0}{1}".format(i, j), SF=1, n=0, T=1)
    G.add_edges_from([("s{0}".format(i), "c{0}{1}".format(i, j))],
                     at=2)  # at=2 function
    G.add_edges_from([("s{0}".format(j), "c{0}{1}".format(i, j))],
                     at=2)  # at=2 function


#"""*****************************************************"""
#***************************### virtual envirenement : n=1
## definition of coarse Vi nodes
def v_env(G, nb):

    i = 1
    while i <= nb:
        G.add_node("V%i" % i, SF=0, n=1, T=0)
        i = i + 1


## Definition of VNFs


def v_VNFs(G, site, VNF, elasticity, number_elasticity, Nbi):
    # CASE OF ELASTICITY == FALSE
    # The network bridge node

    G.add_node("NB{0}".format(site), SF=1, n=1, T=1)
    if elasticity == False:
        # Virtual docker node and its status(S) and connectivity(C): service

        G.add_node("DC{0}".format(str(VNF)), SF=0, n=1, T=0)
        G.add_node("DC{0}{1}".format(str(VNF), "S"), SF=1, n=1, T=1)
        G.add_node("DC{0}{1}".format(str(VNF), "C"), SF=1, n=1, T=1)

        # Edges for the dokcer VNF nodes

        G.add_edges_from(
            [("DC{0}{1}".format(str(VNF), "S"), "DC{0}".format(str(VNF)))],
            at=1)
        G.add_edges_from(
            [("DC{0}{1}".format(str(VNF), "C"), "DC{0}".format(str(VNF)))],
            at=1)
        G.add_edges_from([("DC{0}{1}".format(str(VNF), "S"), "DC{0}{1}".format(
            str(VNF), "C"))],
                         at=2)
        ## Virtal connection between network bridge and each docker connectivity
        G.add_edges_from(
            [("NB{0}".format(site), "DC{0}{1}".format(str(VNF), "C"))], at=2)

        # Define An "and" edge between the docker and  Vi
        G.add_edges_from([("DC{0}".format(str(VNF)), "V{0}".format(site))],
                         at=1)

        #edge inter layer
        G.add_edges_from([("s{0}".format(site), "DC{0}S".format(str(VNF)))],
                         at=2)

    # CASE OF ELASTICITY == TRUE

    if elasticity == True:
        # Virtual docker node  VNF
        G.add_node("DC{0}".format(str(VNF)), SF=0, n=1, T=0)
        # The edge between the docker node and the Vi
        G.add_edges_from([("DC{0}".format(str(VNF)), "V{0}".format(site))],
                         at=1)

        i = 1
        while i <= number_elasticity:
            # Virtual docker node  that represent the elasticity of VNF
            G.add_node("DC{0}{1}".format(str(VNF), i), SF=0, n=1, T=0)
            G.add_node("ClusterD{0}".format(str(VNF)), SF=0, n=1, T=0)
            G.add_node("DC{0}{1}{2}".format(str(VNF), i, "S"), SF=1, n=1, T=1)

            G.add_node("DC{0}{1}{2}".format(str(VNF), i, "C"), SF=1, n=1, T=1)

            # Edges between docker node  that represent the elasticity of VNF
            G.add_edges_from([("DC{0}{1}".format(
                str(VNF), i), "ClusterD{0}".format(str(VNF)))],
                             at=0)  # at=0 for "or" --> elasticity
            G.add_edges_from(
                [("ClusterD{0}".format(str(VNF)), "DC{0}".format(str(VNF)))],
                at=1)  # at=1 for "and clusterD" --> elasticity

            G.add_edges_from([("DC{0}{1}{2}".format(
                str(VNF), i, "S"), "DC{0}".format(str(VNF)))],
                             at=1)
            G.add_edges_from([("DC{0}{1}{2}".format(
                str(VNF), i, "C"), "DC{0}".format(str(VNF)))],
                             at=1)
            G.add_edges_from([("DC{0}{1}{2}".format(
                str(VNF), i, "S"), "DC{0}{1}{2}".format(str(VNF), i, "C"))],
                             at=2)
            ## Virtal connection between network bridge and each docker connectivity
            G.add_edges_from([("NB{0}".format(site), "DC{0}{1}{2}".format(
                str(VNF), i, "C"))],
                             at=2)
            #edge inter layer
            G.add_edges_from(
                [("s{0}".format(site), "DC{0}{1}S".format(str(VNF), i))], at=2)

            i = i + 1


###********************************* OVERLAY NETWORK
def OVERLAY(G, site1, site2, etcd1_bool, num1, etcd1, etcd2_bool, num2, etcd2,
            xcpt):  # cpt of X num for etcd elasticity
    # define overlay knowledge graph
    G.add_node("OV{0}{1}".format(site1, site2), SF=0, n=1, T=0)
    # OVS Overlay status
    G.add_node("OV{0}{1}S".format(site1, site2), SF=1, n=1, T=1)
    # OVC : Overlay Ei and Ej converged
    G.add_node("OV{0}{1}C".format(site1, site2), SF=1, n=1, T=1)
    ## Add the edges
    # Bteween OVS-->OV
    G.add_edges_from(
        [("OV{0}{1}S".format(site1, site2), "OV{0}{1}".format(site1, site2))],
        at=1)
    # Bteween OVC-->OV
    G.add_edges_from(
        [("OV{0}{1}C".format(site1, site2), "OV{0}{1}".format(site1, site2))],
        at=1)
    G.add_edges_from(
        [("OV{0}{1}S".format(site1, site2), "OV{0}{1}C".format(site1, site2))],
        at=2)
    if etcd1_bool == True:
        if num1 == 1:
            G.add_edges_from(
                [("DC{0}".format(etcd1), "OV{0}{1}".format(site1, site2))],
                at=1)
        else:
            G.add_node("cluster{0}".format(etcd1), at=0, n=2, T=0)
            G.add_edges_from(
                [("cluste{0}".format(etcd1), "OV{0}{1}".format(site1, site2))],
                at=1)
            i = 1
            while i <= num1:
                G.add_edges_from([("DC{0}{1}".format(
                    etcd1, i), "cluster{0}".format(etcd1))],
                                 at=0)
                i = i + 1
            xcpt = xcpt + 1

    if etcd2_bool == True:

        if num2 == 1:
            G.add_edges_from(
                [("DC{0}".format(etcd2), "OV{0}{1}".format(site1, site2))],
                at=1)
        else:
            G.add_node("cluster{0}".format(etcd2), at=0, n=2, T=0)
            G.add_edges_from([("cluster{0}".format(etcd2), "OV{0}{1}".format(
                site1, site2))],
                             at=1)
            i = 1
            while i <= num2:
                G.add_edges_from([("DC{0}{1}".format(
                    etcd1, i), "cluster{0}".format(etcd2))],
                                 at=0)
                i = i + 1
            xcpt = xcpt + 1
    return xcpt


#********************** application layer n=2
def A_VNFs(G, site, VNF, elasticity, number_elasticity, monit, etcd_bool, etcd,
           xcpt, typeN):  # entry etcd== To wich etcd it is linked
    if typeN != "Docker_ETCD":
        if elasticity == False:
            ## define the app and process nodes
            G.add_node("App{0}".format(str(VNF)), SF=0, n=2, T=1)
            G.add_node("P{0}".format(str(VNF)), SF=2, n=2, T=1)
            ## define the edges between the app and processes

            G.add_edges_from(
                [("P{0}".format(str(VNF)), "App{0}".format(str(VNF)))], at=1)
            #edge inter layer
            G.add_edges_from(
                [("DC{0}S".format(str(VNF)), "App{0}".format(str(VNF)))], at=2)

            if etcd_bool == True:
                # Define the node ETCD client
                G.add_node(
                    "P{0}EC".format(str(VNF)), SF=2, n=2, T=1
                )  # ETCD Client (EC) # SF=2 spontaneous fault with auto recovery
                # Define the edge between ETCD client and App
                G.add_edges_from(
                    [("P{0}EC".format(str(VNF)), "App{0}".format(str(VNF)))],
                    at=1)
            if monit == True:
                G.add_node("P{0}M".format(str(VNF)), SF=1, n=2,
                           T=1)  # M for monit
                # define the edges between monit and process
                G.add_edges_from(
                    [("P{0}M".format(str(VNF)), "P{0}".format(str(VNF)))],
                    at=3)  # for monit at=3 == (monit) implique (processes)
                if etcd_bool == True:
                    G.add_edges_from([("P{0}M".format(
                        str(VNF)), "P{0}EC".format(str(VNF)))],
                                     at=3)

        if elasticity == True:
            G.add_node("App{0}".format(str(VNF)), SF=0, n=2, T=1)
            ## inter layer status dependencies with x
            G.add_node("clusterS{0}".format(VNF), SF=0, n=2, T=0)
            G.add_node("clusterA{0}".format(VNF), SF=0, n=2, T=0)
            G.add_edges_from(
                [("clusterS{0}".format(VNF), "App{0}".format(VNF))],
                at=2)  # not(x) --> not(app)
            G.add_edges_from(
                [("clusterA{0}".format(VNF), "App{0}".format(VNF))], at=1)
            i = 1
            while i <= number_elasticity:
                G.add_edges_from(
                    [("DC{0}{1}S".format(str(VNF),
                                         i), "clusterS{0}".format(VNF))],
                    at=0)  # not(x) --> not(app) with x = DC1 orDC2

                G.add_node("App{0}{1}".format(str(VNF), i), SF=0, n=2, T=1)
                G.add_node("P{0}{1}".format(str(VNF), i), SF=2, n=2, T=1)

                # Define the edges between the APP and processes / App cluster and Appij
                G.add_edges_from([("App{0}{1}".format(
                    str(VNF), i), "clusterA{0}".format(str(VNF)))],
                                 at=0)  # at=0 --> or
                G.add_edges_from([("P{0}{1}".format(
                    str(VNF), i), "App{0}{1}".format(str(VNF), i))],
                                 at=1)
                if etcd_bool == True:
                    G.add_node("P{0}{1}EC".format(str(VNF), i), SF=2, n=2,
                               T=1)  # ETCD Client (EC)
                    # Define the edge between Process client and App
                    G.add_edges_from([("P{0}{1}EC".format(
                        str(VNF), i), "App{0}{1}".format(str(VNF), i))],
                                     at=1)
                if monit == True:
                    G.add_node("P{0}{1}M".format(str(VNF), i), SF=1, n=2,
                               T=1)  # M for monit

                    G.add_edges_from([("P{0}{1}M".format(
                        str(VNF), i), "P{0}{1}".format(str(VNF), i))],
                                     at=3)  ## at=3 for monit
                    if etcd_bool == True:
                        G.add_edges_from([("P{0}{1}M".format(
                            str(VNF), i), "P{0}{1}EC".format(str(VNF), i))],
                                         at=3)
                i = i + 1
            xcpt = xcpt + 1
    else:

        if elasticity == False:
            G.add_node("App{0}".format(str(VNF)), SF=0, n=2, T=1)
            # Define the node for the memory cash exception
            G.add_node("Memory{0}".format(str(VNF)), SF=1, n=2, T=0)
            G.add_node("ClusterEvent{0}".format(str(VNF)), SF=0, n=2, T=0)

            G.add_edges_from([("App{0}".format(
                str(VNF)), "ClusterEvent{0}".format(str(VNF)))],
                             at=0)
            G.add_edges_from([("Memory{0}".format(
                str(VNF)), "ClusterEvent{0}".format(str(VNF)))],
                             at=0)
            #edge inter layer
            G.add_edges_from(
                [("DC{0}S".format(str(VNF)), "App{0}".format(str(VNF)))], at=2)
        if elasticity == True:
            G.add_node("App{0}".format(str(VNF)), SF=0, n=2, T=1)
            ## inter layer status dependencies with x
            G.add_node("clusterS{0}".format(VNF), SF=0, n=2, T=0)
            G.add_node("clusterA{0}".format(VNF), SF=0, n=2, T=0)
            G.add_edges_from(
                [("clusterS{0}".format(VNF), "App{0}".format(VNF))],
                at=2)  # not(x) --> not(app)
            G.add_edges_from(
                [("clusterA{0}".format(VNF), "App{0}".format(VNF))],
                at=1)  # not(x) --> not(app)
            # Define the node for the memory cash exception
            G.add_node("Memory{0}".format(str(VNF)), SF=1, n=2, T=0)
            G.add_node("ClusterEvent{0}".format(str(VNF)), SF=1, n=2, T=0)

            G.add_edges_from([("App{0}".format(
                str(VNF)), "ClusterEvent{0}".format(str(VNF)))],
                             at=0)
            G.add_edges_from([("Memory{0}".format(
                str(VNF)), "ClusterEvent{0}".format(str(VNF)))],
                             at=0)
            i = 1
            while i <= number_elasticity:
                G.add_edges_from(
                    [("DC{0}{1}S".format(str(VNF),
                                         i), "clusterS{0}".format(VNF))],
                    at=0)  # not(x) --> not(app) with x = DC1 orDC2

                G.add_node("App{0}{1}".format(str(VNF), i), SF=0, n=2, T=1)
                G.add_edges_from([("App{0}{1}".format(
                    str(VNF), i), "clusterA{0}".format(str(VNF)))],
                                 at=0)  # at=0 --> or

    return xcpt


#***********************************
# Local Application Connectivity :in same site
def LA_con(G, VNF1, elasticity1_bool, num1, VNF2, elasticity2_bool, num2,
           etcd_bool, elasticity3_bool, num3, etcd, xcpt):
    G.add_node("C{0}{1}".format(str(VNF1), str(VNF2)), SF=0, n=2, T=1)
    ## define the edges
    G.add_edges_from(
        [("App{0}".format(str(VNF1)), "C{0}{1}".format(str(VNF1), str(VNF2)))],
        at=1)
    G.add_edges_from(
        [("App{0}".format(str(VNF2)), "C{0}{1}".format(str(VNF1), str(VNF2)))],
        at=1)
    if etcd_bool == True:
        G.add_edges_from([("ClusterEvent{0}".format(
            str(etcd)), "C{0}{1}".format(str(VNF1), str(VNF2)))],
                         at=1)

        if elasticity3_bool == False:
            G.add_edges_from([("DC{0}C".format(str(etcd)), "C{0}{1}".format(
                str(VNF1), str(VNF2)))],
                             at=1)
        if elasticity3_bool == True:
            G.add_node("cluster{0}".format(etcd), at=0, n=2, T=0)
            G.add_edges_from([("cluster{0}".format(etcd), "C{0}{1}".format(
                str(VNF1), str(VNF2)))],
                             at=1)
            i = 1
            while i <= num3:
                G.add_edges_from([("DC{0}{1}C".format(
                    str(etcd), i), "cluster{0}".format(etcd))],
                                 at=0)
                i = i + 1
            xcpt = xcpt + 1
    if elasticity1_bool == False:
        G.add_edges_from([("DC{0}C".format(str(VNF1)), "C{0}{1}".format(
            str(VNF1), str(VNF2)))],
                         at=1)

    if elasticity2_bool == False:
        G.add_edges_from([("DC{0}C".format(str(VNF2)), "C{0}{1}".format(
            str(VNF1), str(VNF2)))],
                         at=1)
    if elasticity1_bool == True:
        G.add_node("clusterC{0}".format(VNF1), at=0, n=2, T=0)
        G.add_edges_from([("clusterC{0}".format(VNF1), "C{0}{1}".format(
            str(VNF1), str(VNF2)))],
                         at=1)
        i = 1
        while i <= num1:
            G.add_edges_from([("DC{0}{1}C".format(
                str(VNF1), i), "clusterC{0}".format(VNF1))],
                             at=0)
            i = i + 1
        xcpt = xcpt + 1
    if elasticity2_bool == True:
        G.add_node("clusterC{0}".format(VNF2), at=0, n=2, T=0)
        G.add_edges_from([("clusterC{0}".format(VNF2), "C{0}{1}".format(
            str(VNF1), str(VNF2)))],
                         at=1)
        i = 1
        while i <= num2:
            G.add_edges_from([("DC{0}{1}C".format(
                str(VNF2), i), "clusterC{0}".format(VNF2))],
                             at=0)
            i = i + 1
        xcpt = xcpt + 1

    return xcpt


# Distant Application Connectivity: in different sites
def DA_con(G, site1, site2, VNF1, elasticity1_bool, num1, VNF2,
           elasticity2_bool, num2, etcd_bool, elasticity3_bool, num3, etcd,
           etcdM_bool, elasticity4_bool, num4, etcdM, xcpt):
    G.add_node("C{0}{1}".format(VNF1, VNF2), SF=0, n=2, T=1)
    ## define the edges
    G.add_edges_from([("App{0}".format(VNF1), "C{0}{1}".format(VNF1, VNF2))],
                     at=1)
    G.add_edges_from([("App{0}".format(VNF2), "C{0}{1}".format(VNF1, VNF2))],
                     at=1)
    if etcd_bool == True:
        G.add_edges_from(
            [("ClusterEvent{0}".format(etcd), "C{0}{1}".format(VNF1, VNF2))],
            at=1)
    if etcdM_bool == True:
        G.add_edges_from(
            [("ClusterEvent{0}".format(etcdM), "C{0}{1}".format(VNF1, VNF2))],
            at=1)

    if elasticity1_bool == False:
        G.add_edges_from(
            [("DC{0}C".format(VNF1), "C{0}{1}".format(VNF1, VNF2))], at=1)

    if elasticity2_bool == False:
        G.add_edges_from(
            [("DC{0}C".format(VNF2), "C{0}{1}".format(VNF1, VNF2))], at=1)
    if elasticity1_bool == True:
        G.add_node("clusterC{0}".format(VNF1), SF=0, n=2, T=0)
        G.add_edges_from(
            [("clusterC{0}".format(VNF1), "C{0}{1}".format(VNF1, VNF2))], at=1)
        i = 1
        while i <= num1:
            G.add_edges_from(
                [("DC{0}{1}C".format(VNF1, i), "clusterC{0}".format(VNF1))],
                at=0)
            i = i + 1
        xcpt = xcpt + 1
    if elasticity2_bool == True:
        G.add_node("clusterC{0}".format(VNF2), SF=0, n=2, T=0)
        G.add_edges_from(
            [("clusterC{0}".format(VNF2), "C{0}{1}".format(VNF1, VNF2))], at=1)
        i = 1
        while i <= num2:
            G.add_edges_from(
                [("DC{0}{1}C".format(VNF2, i), "clusterC{0}".format(VNF2))],
                at=0)
            i = i + 1
        xcpt = xcpt + 1
    #add the overlay:
    G.add_edges_from(
        [("OV{0}{1}".format(site1, site2), "C{0}{1}".format(VNF1, VNF2))],
        at=1)
    return xcpt


def service(G, service, list):

    #list= list of nodes in the service
    G.add_node("{0}".format(str(service)), SF=0, n=3, T=1)  # n=3 service layer
    for e in list:
        G.add_edges_from([("App{0}".format(str(e)), "{0}".format(service))],
                         at=1)  # and
    G.add_edges_from(
        [("C{0}{1}".format(list[0], list[1]), "{0}".format(service))],
        at=1)  # Connection Bono to Sprout
    G.add_edges_from(
        [("C{0}{1}".format(list[1], list[2]), "{0}".format(service))],
        at=1)  # Connection Sprout to homestead
    G.add_edges_from(
        [("C{0}{1}".format(list[2], list[3]), "{0}".format(service))],
        at=1)  # Connection homestead to cass


"""if __name__ == "__main__" :

    
 G = nx.DiGraph()
 Sites(G,3) 
 PCon_Sites(G, 1,2)
 #A_services(G,1,"bono1",True,2,True,True,"E1")
 OVERLAY(G,1,2,True,"etcd1",True,"etcd2") 
 print(G.nodes())
 print G.edges() """
