#!/usr/bin/env python3
import yaml
import networkx as nx
import Bknowledge as BK


def yaml_loader(filepath):
    with open(filepath, "r") as topo:
        data = yaml.load(topo)
    return data


def yaml_dump(filepath, data):
    yaml.dump(data, topo)


def global_graph(PATH):

    # Define the graph
    G = nx.DiGraph()
    # Define the xcpt for x var type
    xcpt = 1
    # get the data from the file
    filepath = str(PATH)
    data = yaml_loader(filepath)
    ## get the number of sites
    #site_num=data["sites-number"][0]
    #site_num=site_num['nb']
    #print(site_num)
    ## define the dictionary of services: elastcity
    Edico = {}
    Sdico = {}
    Ssdico = {}
    # Dfine the dico of VNF types
    Tdico = {}
    i = 1
    scpt = 1
    list = []
    Bono_list = []
    data = data["Sites"]
    site_num = 0
    while i <= len(data):

        l = data["site%i" % i]["VNFs"]

        j = 0
        while j < len(l):
            xx = l[j]
            name = xx["VNF"][0]["Name"]
            if "bono" in name:
                Bono_list.append(name)
            num_DC = xx["VNF"][4]["nb_VDcon"]
            num_LC = xx["VNF"][3]["nb_VLcon"]
            num_type = num_DC + num_LC + 5
            type_docker = xx["VNF"][num_type]["Type"]
            Tdico[str(name)] = type_docker
            elasticity = xx["VNF"][1]["nb"]
            Edico[(i, str(name))] = elasticity
            Sdico[str(name)] = i

            Ssdico[str(name)] = j

            j = j + 1

        i = i + 1
    site_num = i - 1

    ####"*****************************************************************************************************"
    #*******************************create the physical layer and virtual Vi nodes

    i = 1
    while i <= len(data):
        ## define the sites and virtal env
        BK.Sites(G, site_num)
        BK.v_env(G, site_num)

        ## P_con
        xx = data["site%i" % i]["Networks"][2]
        num_Pcon = xx["nb_Pcon"]

        k = 1
        while k <= num_Pcon:
            #### Define the physical connectivity and overlays
            n = 2 + k
            xx = data["site%i" % i]["Networks"][n]
            Pcon = xx["Pcon"]
            BK.PCon_Sites(G, i, Pcon)
            ### Define the overlay connectivity
            ### ETCD for site 1
            xx = data["site%i" % i]["Networks"][1]
            etcd = xx["etcd"]
            if etcd != "None":
                etcd_bool = True
            else:
                etcd_bool = False
            ## etcd elasticity from dico

            num1 = Edico[(i, str(etcd))]
            ### ETCD for site 2
            xx = data["site{0}".format(Pcon)]["Networks"][1]
            etcd2 = xx["etcd"]
            if etcd2 != "None":
                etcd2_bool = True
            else:
                etcd2_bool = False
            xx = data["site%i" % i]["Networks"][1]
            num2 = Edico[(Pcon, str(etcd2))]
            #Define the overlay for each Pcon
            xcpt = BK.OVERLAY(G, i, Pcon, etcd_bool, num1, etcd, etcd2_bool,
                              num2, etcd2, xcpt)

            k = k + 1
        i = i + 1
    i = 1
    while i <= site_num:

        # number of VNFs in site i
        l = data["site%i" % i]["VNFs"]
        num_VNF = len(l)
        #print(num_VNF)

        # get VNFs:
        j = 0
        while j < num_VNF:

            ### Get the VNF
            t = {}
            t = data["site%i" % i]["VNFs"][j]
            VNF = t["VNF"][0]["Name"]
            ### Get the elasticity
            number_elasticity = t["VNF"][1]["nb"]
            if number_elasticity > 1:
                elasticity = True
            else:
                elasticity = False
            ### get the distant connectivity
            num_VLcon = t["VNF"][3]["nb_VLcon"]
            num_VDcon = t["VNF"][4]["nb_VDcon"]

            num_num_lignes = num_VDcon + num_VLcon + 5
            type_docker = t["VNF"][num_num_lignes]["Type"]

            monit = t["VNF"][2]["monit"]
            xx = data["site%i" % i]["Networks"][0]
            Nbi = xx["Network_bridge"]
            xx = data["site%i" % i]["Networks"][1]
            etcd = xx["etcd"]

            num3 = Edico[(i, str(etcd))]

            if num3 > 1:
                elasticity3_bool = True
            else:
                elasticity3_bool = False
            if etcd != "None":
                etcd_bool = True
            else:
                etcd_bool = False
            ## Define the virtual nodes
            BK.v_VNFs(G, site_num, VNF, elasticity, number_elasticity, Nbi)
            ## Define the application nodes

            xcpt = BK.A_VNFs(G, site_num, VNF, elasticity, number_elasticity,
                             monit, etcd_bool, etcd, xcpt, type_docker)

            # Local Application Connectivity :in same site

            m = 1

            while m <= num_VLcon:
                l = m + 4

                VNF2 = t["VNF"][l]["VLcon"]
                site2 = Sdico[str(VNF2)]
                num2 = Edico[(site2, str(VNF2))]
                if num2 > 1:
                    elasticity2_bool = True
                else:
                    elasticity2_bool = False

                xcpt = BK.LA_con(G, VNF, elasticity, number_elasticity, VNF2,
                                 elasticity2_bool, num2, etcd_bool,
                                 elasticity3_bool, num3, etcd, xcpt)

                m = m + 1
            # Distant Application Connectivity: in different sites
            q = 1
            while q <= num_VDcon:
                l = 4 + num_VLcon + q

                VNF2 = t["VNF"][l]["VDcon"]

                #print(VNF2)
                site2 = Sdico[str(VNF2)]
                #print(site2)
                num2 = Edico[(site2, str(VNF2))]
                if num2 > 1:
                    elasticity2_bool = True
                else:
                    elasticity2_bool = False
                xx = data["site{0}".format(site2)]["Networks"][1]
                etcdM = xx["etcd"]
                num4 = Edico[(site2, str(etcdM))]

                if num4 > 1:
                    elasticity4_bool = True
                else:
                    elasticity4_bool = False
                if etcdM != "None":
                    etcdM_bool = True
                else:
                    etcdM_bool = False

                xcpt = BK.DA_con(G, i, site2, VNF, elasticity,
                                 number_elasticity, VNF2, elasticity2_bool,
                                 num2, etcd_bool, elasticity3_bool, num3, etcd,
                                 etcdM_bool, elasticity4_bool, num4, etcdM,
                                 xcpt)

                q = q + 1
            j = j + 1
        i = i + 1
    # Define the register services:
    cpt_register = 1
    Register_Services = []
    for e in Bono_list:
        Register_Services.append(str(e))
        cpt_register = Service_Register_modeling(G, PATH, Register_Services,
                                                 cpt_register)
        cpt_register = cpt_register + 1
        del Register_Services[:]

    return G


# function to create


def topology_graph_call(path):

    # Define the graph
    Topo = nx.DiGraph()

    # get the data from the file
    filepath = str(path)
    data = yaml_loader(filepath)
    ## get the number of sites
    data = data["Sites"]
    site_num = len(data)
    ########################### defiine the VNFs########################################
    #######################################################################################
    i = 1
    while i <= site_num:
        l = data["site%i" % i]["VNFs"]
        num_VNF = len(l)
        j = 0
        while j < num_VNF:
            ## define te register service
            ### create services nodes

            xx = data["site%i" % i]["VNFs"][j]
            name = xx["VNF"][0]["Name"]
            nb_VLcon = xx["VNF"][3]["nb_VLcon"]
            nb_VDcon = xx["VNF"][4]["nb_VDcon"]
            if "homer" in name:
                Topo.add_node("{0}".format(str(name)), at=4)
            else:
                Topo.add_node("{0}".format(str(name)))

            f = 5
            ff = 4 + nb_VLcon
            while f <= ff:

                scon = xx["VNF"][f]["VLcon"]
                Topo.add_edges_from([("{0}".format(name), "{0}".format(scon))])
                f = f + 1

            ff = 4 + nb_VLcon + nb_VDcon
            while f <= ff:
                scon = xx["VNF"][f]["VDcon"]
                Topo.add_edges_from([("{0}".format(name), "{0}".format(scon))])
                f = f + 1
            j = j + 1
        i = i + 1

    return (Topo)


# function to delete "homer" and "ETCD" from the register nodes
def topology_graph_Register(path):

    Topo_R = topology_graph_call(path)
    dic = []
    for e in Topo_R.nodes():
        dic.append(e)
    j = 0

    while j < len(dic):

        if "homer" in str(dic[j]):
            Topo_R.remove_node(dic[j])
        if "E" in str(dic[j]):
            Topo_R.remove_node(dic[j])
        j = j + 1
    return (Topo_R)


def Service_Register_Nodes(
        G, path, liste, cpt
):  ## liste of nodes in Register, and the first bono and last element in liste , cpt for register
    Topo_R = topology_graph_Register(path)
    cpt2 = 0
    first_element = liste[0]
    last_element = liste[-1]
    z = []
    for e in liste:
        z.append(e)
    Register = {}
    w = nx.descendants(Topo_R, last_element)
    for e in w:
        z.append(e)

    leaves = []
    F = nx.subgraph(Topo_R, z)

    for n in F.nodes():
        if F.out_degree(n) == 0:
            leaves.append(n)

    for e in leaves:
        for path in nx.all_simple_paths(F, source=first_element, target=e):
            Register[cpt2] = path
            cpt2 = cpt2 + 1  ## number of registers that has the same nodes in the observations

    return (Topo_R, Register, cpt2)


def Service_Register_modeling(G, path, liste, cpt):

    Topo_R, Register, cpt2 = Service_Register_Nodes(G, path, liste, cpt)

    i = 0
    while i < cpt2:
        Reg = "Register{0}{1}".format(cpt, int(i + 1))

        BK.service(G, str(Reg), Register[i])
        i = i + 1
    return (cpt2)  # return the number of register


"""def Service_Call_modeling(G,path,liste,num_reg, cpt2_reg, num_call): #number of register and call service and the number of register path found for each register observed
  
   Topo= topology_graph_call(path)
   
   list=[]
   i=1
   while i <= cpt2_reg:
      list.append("Register{0}{1}".format(num_reg,int(i)))
      i=i+1

   call= "Call{0}".format(num_call)   
   BK.service(G,str(call),list)
"""
