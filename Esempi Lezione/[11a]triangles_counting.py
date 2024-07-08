

import networkx as nx
# import matplotlib.pyplot as plt

# from timeit import default_timer as timer

if __name__ == "__main__":  
    
    for vertex_set_size in [10,100,1000]:
        print("==Vertices:",vertex_set_size)
        print("ERDOS")
        nxGraph = nx.fast_gnp_random_graph(vertex_set_size,0.4)
        t = nx.triangles(nxGraph)
        pos=nx.spring_layout(nxGraph)
        nx.draw(nxGraph,pos, node_color='orange')
        nx.draw_networkx_labels(nxGraph,pos)
        n = nxGraph.number_of_nodes()
        m = nxGraph.number_of_edges()
        n_triangoli = round(sum(t.values())/3)
        n_attesi = round((4/3)*pow(m/n,3))
        print("N_Triangles:",n_triangoli)
        print("Expected:",n_attesi)
        print("Ratio:",round(n_attesi/n_triangoli,2))
        
        print("NON ERDOS")
        nxGraph = nx.random_internet_as_graph(vertex_set_size)
        t = nx.triangles(nxGraph)
        pos=nx.spring_layout(nxGraph)
        nx.draw(nxGraph,pos, node_color='orange')
        nx.draw_networkx_labels(nxGraph,pos)
        n = nxGraph.number_of_nodes()
        m = nxGraph.number_of_edges()
        n_triangoli = round(sum(t.values())/3)
        n_attesi = round((4/3)*pow(m/n,3))
        
        print("N_Triangles:",n_triangoli)
        print("Expected:",n_attesi)
        print("Ratio:",round(n_attesi/n_triangoli,2))
