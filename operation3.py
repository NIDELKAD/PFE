from st_aggrid import AgGrid
import dimacs
import streamlit as st
import pandas as pd
from random import choice
from fonctions import get_graph_dic, animate
    
def display_op3():

    if "graph_dic" not in st.session_state:
        st.session_state["graph_dic"] = {}

    graph_list = dimacs.graph_list + st.session_state.local_graphs
    graph_name_list = [graph.name for graph in graph_list]

    st.markdown("# Associez à chaque graphe un sommet")

    column1, column2 = st.columns([7,3])

    c1, c2 = column1.columns(2)
    
    graph_name = c1.selectbox(label="Choisir un graphe", options=graph_name_list)
    graph_item = [graph for graph in graph_list if graph.name == graph_name][0]

    if not graph_item.graph_dic:
        get_graph_dic(graph_item)

    # liste qui contient tous les sommets non isolés
    tempo_list = sorted([i for i,j in graph_item.graph_dic.items() if j])  
    
    vertex_item = c2.selectbox(label="Choisir un sommet", options=tempo_list)

    c1, c2, c3, c4 = column1.columns(4)
    subbmit_button = c1.button("Valider")
    delete_button = c2.button("Supprimer")
    random_vertex_button = c3.button("Aléatoire")
    reset_button = c4.button("Rénitialiser")

    if subbmit_button:
        if not graph_item:
            st.toast('Veuillez séléctionner un graphe', icon='❌')
        elif not vertex_item:
            st.toast('Veuillez séléctionner un sommet', icon='❌')
        else:
            st.session_state.graph_dic[graph_item] = vertex_item
            st.toast('Ajout avec succès', icon="✅")
    
    if delete_button:
        if graph_item not in st.session_state.graph_dic.keys():
            st.toast('Graphe non séléctionné, impossible de le supprimer', icon='❌')
        else:
            del st.session_state.graph_dic[graph_item]
            st.toast('Suppression avec succès', icon="✅")

    if random_vertex_button:
        graph_item = choice([graph for graph in graph_list if graph not in st.session_state.graph_dic.keys()])
        if not graph_item.graph_dic:
            get_graph_dic(graph_item)
        vertex_item = choice(list(graph_item.graph_dic.keys()))
        st.session_state.graph_dic[graph_item] = vertex_item

    if reset_button:
        st.session_state.graph_dic.clear()

    # Créer le DataFrame
    graph_name_list = [graph.name for graph in st.session_state.graph_dic.keys()]
    df = pd.DataFrame({"Graphe" : graph_name_list,
                      "Sommet" : st.session_state.graph_dic.values()})
    
    # Affichage des résultats
    
    with column1:
        AgGrid(df, fit_columns_on_grid_load=True, height=150)

    with column2:
        animate("Components/associate.json", 300, 300)

    return st.session_state.graph_dic