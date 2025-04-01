import ALGOS.SA_fonctions as SA
import ALGOS.GA_fonctions as GA
import ALGOS.ACO_fonctions as ACO
import streamlit as st
import constants as cst

def maximum_clique(graph, p, timer, option):
    
    if option == 1:
        st.write(f"Application du {cst.algorithms[0]} ...")
        maximum_clique, calcul_time = SA.maximum_clique_finder(graph.graph_dic, 
                                                               p[0], p[1], p[2],
                                                               timer)
    elif option == 2:
        st.write(f"Application de l'{cst.algorithms[1]} ...")
        maximum_clique, calcul_time = GA.maximum_clique_finder(graph.graph_dic, 
                                                               p[0], p[1], p[2], p[3],
                                                               timer)
    else:
        st.write(f"Application de l'algorithme des {cst.algorithms[2]} ...")
        maximum_clique, calcul_time = ACO.maximum_clique_finder(graph.graph_dic, 
                                                                p[0], p[1], p[2], p[3], p[4],
                                                                timer)
        print("test 2")
    return maximum_clique, calcul_time

def all_clique(graph, p, timer, option):

    if option == 1:
        st.write(f"Application du {cst.algorithms[0]} ...")
        all_clique_found, calcul_time = SA.all_clique_finder(graph.graph_dic, 
                                                             p[0], p[1], p[2],
                                                             timer)    
    elif option == 2:
        st.write(f"Application de l'{cst.algorithms[1]} ...")
        all_clique_found, calcul_time = GA.all_clique_finder(graph.graph_dic, 
                                                             p[0], p[1], p[2], p[3],
                                                             timer)
    else:
        st.write(f"Application de l'algorithme des {cst.algorithms[2]} ...")
        all_clique_found, calcul_time = ACO.all_clique_finder(graph.graph_dic, 
                                                             p[0], p[1], p[2], p[3], p[4],
                                                             timer)   
    return all_clique_found, calcul_time


def vertex_maximum_clique(graph, vertex, p, timer, option):

    if option == 1:
        st.write(f"Application du {cst.algorithms[0]} ...")
        maximum_clique, calcul_time = SA.vertex_maximum_clique_finder(graph.graph_dic, 
                                                                      vertex, 
                                                                      p[0], p[1], p[2],
                                                                      timer)
    
    elif option == 2:
        st.write(f"Application de l'{cst.algorithms[1]} ...")
        maximum_clique, calcul_time = GA.vertex_maximum_clique_finder(graph.graph_dic, 
                                                                      vertex, 
                                                                      p[0], p[1], p[2], p[3],
                                                                      timer)
    
    else:
        st.write(f"Application de l'algorithme des {cst.algorithms[2]} ...")
        maximum_clique, calcul_time = ACO.vertex_maximum_clique_finder(graph.graph_dic, 
                                                                       vertex, 
                                                                       p[0], p[1], p[2], p[3], p[4],
                                                                       timer)
    return maximum_clique, calcul_time
