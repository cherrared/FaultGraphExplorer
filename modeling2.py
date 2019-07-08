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


if __name__ == "__main__":

    # Define the graph
    G = nx.DiGraph()
    # Define the xcpt for x var type
    xcpt = 1
    # get the data from the file
    filepath = "./input-topo.yml"
    data = yaml_loader(filepath)
    ## get the number of sites
    site_num = data["sites-number"][0]
    site_num = site_num['nb']
    #print(site_num)
    ## define the dictionary of services: elastcity
    Edico = {}
    Sdico = {}
    i = 1
    while i <= site_num:

        l = data["site%i" % i]["Services_type_number"][0]
        num_service = l["nb"]
        j = 0
        while j < num_service:
            xx = data["site%i" % i]["Services"][j]
            name = xx["Service"][0]["Name"]
            elasticity = xx["Service"][1]["nb"]
            Edico[(i, str(name))] = elasticity
            Sdico[str(name)] = i
            j = j + 1

        i = i + 1

    ####"*****************************************************************************************************"
    #*******************************create the physical layer and virtual Vi nodes

    i = 1
    while i <= site_num:
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

        # number of services in site i
        l = data["site%i" % i]["Services_type_number"][0]
        num_service = l["nb"]
        #print(num_service)

        # get services:
        j = 0
        while j < num_service:

            ### Get the service
            t = {}
            t = data["site%i" % i]["Services"][j]
            service = t["Service"][0]["Name"]
            ### Get the elasticity
            number_elasticity = t["Service"][1]["nb"]
            if number_elasticity > 1:
                elasticity = True
            else:
                elasticity = False
            ### get the distant connectivity
            num_VLcon = t["Service"][3]["nb_VLcon"]
            num_VDcon = t["Service"][4]["nb_VDcon"]

            monit = t["Service"][2]["monit"]
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
            BK.v_services(G, site_num, service, elasticity, number_elasticity,
                          Nbi)
            ## Define the application nodes

            xcpt = BK.A_services(G, site_num, service, elasticity,
                                 number_elasticity, monit, etcd_bool, etcd,
                                 xcpt)

            # Local Application Connectivity :in same site
            m = 1
            while m <= num_VLcon:
                l = m + 4
                #print("***************")
                #print(l)

                service2 = t["Service"][l]["VLcon"]
                site2 = Sdico[str(service2)]
                num2 = Edico[(site2, str(service2))]
                if num2 > 1:
                    elasticity2_bool = True
                else:
                    elasticity2_bool = False

                xcpt = BK.LA_con(G, service, elasticity, number_elasticity,
                                 service2, elasticity2_bool, num2, etcd_bool,
                                 elasticity3_bool, num3, etcd, xcpt)
                m = m + 1
            # Distant Application Connectivity: in different sites
            q = 1
            while q <= num_VDcon:
                l = 4 + num_VLcon + q

                service2 = t["Service"][l]["VDcon"]
                #print(service2)
                site2 = Sdico[str(service2)]
                #print(site2)
                num2 = Edico[(site2, str(service2))]
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

                xcpt = BK.DA_con(G, i, site2, service, elasticity,
                                 number_elasticity, service2, elasticity2_bool,
                                 num2, etcd_bool, elasticity3_bool, num3, etcd,
                                 etcdM_bool, elasticity4_bool, num4, etcdM,
                                 xcpt)

                q = q + 1
            j = j + 1
        i = i + 1

    print(G.nodes())
    print(G.edges())
