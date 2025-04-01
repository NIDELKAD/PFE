import streamlit as st
import constants as cst
from fonctions import load_graph_dic, operation1_results, operation2_results, operation3_results, display_comparison
from ALGOS import algos as algo

def display_results(operation, graph, vertex, SA_clique, GA_clique, ACO_clique):

    if operation == cst.operations[0]: # Trouver la clique maximal du graphe
        result = operation1_results(graph, SA_clique, GA_clique, ACO_clique)
        
    elif operation == cst.operations[1]: # Localiser toutes les cliques du graphe
        result = operation2_results(graph, SA_clique, GA_clique, ACO_clique)

    else: # Déterminer La clique maximal relié à un nœud
        result = operation3_results(vertex, SA_clique, GA_clique, ACO_clique)

    return result

def apply_algo(operation, graph, algo_list, vertex, SA_settings, GA_settings, ACO_settings, timer):
    
    st.write(f"## Graphe : {graph.name}")
    
    # Initialiser les cliques
    SA_result = None
    GA_result = None
    ACO_result = None

    if operation == cst.operations[0]: # Trouver la clique maximal du graphe
        
        if cst.algorithms[0] in algo_list: # Recuit simulé
            SA_result = algo.maximum_clique(graph, SA_settings, timer, 1)
        
        if cst.algorithms[1] in algo_list: # Algorithme génétique
            GA_result = algo.maximum_clique(graph, GA_settings, timer, 2)
        
        if cst.algorithms[2] in algo_list: # Colonie de fourmis
            ACO_result = algo.maximum_clique(graph, ACO_settings, timer, 3)

    elif operation == cst.operations[1]: # Localiser toutes les cliques du graphe
        
        if cst.algorithms[0] in algo_list: # Recuit simulé
            SA_result = algo.all_clique(graph, SA_settings, timer, 1)
        
        if cst.algorithms[1] in algo_list: # Algorithme génétique
            GA_result = algo.all_clique(graph, GA_settings, timer, 2)
        
        if cst.algorithms[2] in algo_list: # Colonie de fourmis
            ACO_result = algo.all_clique(graph, ACO_settings, timer, 3)

    else: # Déterminer La clique maximal relié à un nœud
        
        if cst.algorithms[0] in algo_list: # Recuit simulé
            SA_result = algo.vertex_maximum_clique(graph, vertex, SA_settings, timer, 1)
        
        if cst.algorithms[1] in algo_list: # Algorithme génétique
            GA_result = algo.vertex_maximum_clique(graph, vertex, GA_settings, timer, 2)
        
        if cst.algorithms[2] in algo_list: # Colonie de fourmis
            ACO_result = algo.vertex_maximum_clique(graph, vertex, ACO_settings, timer, 3)

    return display_results(operation, graph, vertex, SA_result, GA_result, ACO_result)  
        
def run(operation, graph_data, algo_list, SA_settings, GA_settings, ACO_settings, timer):

    if operation != cst.operations[2]:
        load_graph_dic(graph_data)

    result_list = [] # Liste des efficacité de chaque algo appliqué sur chaque graphe
    graph_name_list = [graph.name for graph in graph_data] # Liste des noms des graphes
    
    if operation != cst.operations[2]:
        for graph in graph_data:
            result = apply_algo(operation, graph, algo_list, None, SA_settings, GA_settings, ACO_settings, timer)
            result_list.append(result)
    
    else: # Déterminer La clique maximal relié à un nœud
        for graph, vertex in graph_data.items():
            result = apply_algo(operation, graph, algo_list, vertex, SA_settings, GA_settings, ACO_settings, timer)
            result_list.append(result)

    display_comparison(graph_name_list, algo_list, result_list, operation)
