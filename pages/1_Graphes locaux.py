import streamlit as st
import pandas as pd
from ALGOS.SA_fonctions import maximum_clique_finder
from fonctions import os, json, draw_graph, AgGrid
from settings import display_random_graph_settings, animate
import constants as cst
from random import randint

if "working_directory" not in st.session_state:
    st.session_state["working_directory"] = cst.working_directory_path

if "created_graph" not in st.session_state:
    st.session_state["created_graph"] = {}

if "random_created_graph" not in st.session_state:
    st.session_state["random_created_graph"] = {}

st.set_page_config(layout="wide")

os.environ["PATH"] += os.pathsep + cst.graphiz_bin_path
  
# Télécharger le graphe créé (met les graphes dans les dossiers correspondants)

def download_graph(graph_name, clique_size, dot_element, option):

    if option == 1: # création manuelle
        directory_name1 = st.session_state.working_directory + "\Graphes\Manual\JSON"
        directory_name2 = st.session_state.working_directory + "\Graphes\Manual\Images"
        graph = st.session_state.created_graph
    
    else: # création aléatoire
        directory_name1 = st.session_state.working_directory + "\Graphes\Random\JSON"
        directory_name2 = st.session_state.working_directory + "\Graphes\Random\Images"
        graph = st.session_state.random_created_graph

    filename = graph_name + ".json"
    filepath = os.path.join(directory_name1, filename)

    if os.path.exists(filepath):
        st.toast("Nom de graphe déjà pris", icon="❌")

    else: # créer les fichiers .png et .json
        
        edges = 0 # nombre d'arrêtes du graphe
        for i in graph.values():
            edges += len(i)

        data = {
            'name': graph_name,
            'nodes': len(graph.keys()),
            'edges': edges,
            'clique_size': clique_size,
            'graph_dic': graph
        }

        # Partie fichier .json

        with open(filepath, 'w', newline='') as f:
            json.dump(data, f)
        
        # Partie fichier .png
        
        dot_element.render(directory = directory_name2, 
                            filename=graph_name, 
                            format="png", 
                            cleanup=True)
        
        st.toast("Graphe ajouté avec succès", icon="✅")

#------------------------- Fonctions pour la création manuelle de graphes -----------------------------

# Ajouter un sommet et ses voisins

def add_vertex_func(sommet_val, voisin_list):

    dic_keys = list(st.session_state.created_graph.keys())
    st.session_state.created_graph[sommet_val] = voisin_list
    
    for v in voisin_list:
        if v not in dic_keys:
            st.session_state.created_graph[v] = [sommet_val]
        else:
            if sommet_val not in st.session_state.created_graph[v]:
                st.session_state.created_graph[v].append(sommet_val)

    for i, j in st.session_state.created_graph.items():
        for k in j:
            if i not in st.session_state.created_graph[k]:
                j.remove(k)

# Supprimer un sommet

def del_vertex_func(sommet_val):

    if sommet_val in st.session_state.created_graph:

        neighbors = st.session_state.created_graph[sommet_val]

        for neighbor in neighbors:
            st.session_state.created_graph[neighbor].remove(sommet_val)

        del st.session_state.created_graph[sommet_val]
    
    else:
        st.toast(f"{sommet_val} n'existe pas dans le graphe, impossible de le supprimer", icon="❌")

#------------------------------------ Création manuelle de graphes ---------------------------------------

st.markdown("# Graphes locaux")

st.markdown("## Créer un graphe manuellement")

maximum_clique = None

vertex_list = range(1, 101)

c1, c2, c3 = st.columns([2,2,6])

graph_name = c1.text_input("Entrez le nom du graphe : ")

vertex_val = int(c2.selectbox(label="Choisir un sommet", options=vertex_list))

tempo_list = [v for v in vertex_list if v != vertex_val]

if "voisins_list" not in st.session_state:
    st.session_state.voisins_list = []

st.session_state.voisins_list = c3.multiselect(label="Ajouter les voisins", 
                                                options=tempo_list, 
                                                placeholder="Liste des voisins")

c1, c2, c3, c4 = st.columns(4)

add_vertex_button = c1.button("Ajouter sommet")
delete_vertex_button = c2.button("Supprimer sommet")
reset_graph_button = c3.button("Rénitialiser graphe")

if add_vertex_button:
    add_vertex_func(vertex_val, st.session_state.voisins_list)
    vertex_list = [s for s in range(1, 101) if s not in st.session_state.created_graph.keys()]

if delete_vertex_button:
    del_vertex_func(vertex_val)

if reset_graph_button:
    st.session_state.created_graph.clear()

if st.session_state.created_graph:
    maximum_clique, _ = maximum_clique_finder(st.session_state.created_graph, 1500, 0.99, 1000, None)

# Trier le graphe
sorted_created_graph = dict(sorted(st.session_state.created_graph.items()))

# Créer le DataFrame
df = pd.DataFrame(sorted_created_graph.items(), columns=['Sommet', 'Voisins'])

# Convertir les éléments uniques en listes
df['Voisins'] = df['Voisins'].apply(lambda x: [x] if not isinstance(x, list) else x)

# Trier la liste des voisins
df['Voisins'] = df['Voisins'].apply(lambda x: sorted(x))

# Affichage des résultats
c1, c2, c3 = st.columns([3,2,5])

with c1:
    AgGrid(df, fit_columns_on_grid_load=True, height=400)

dot_element = draw_graph(sorted_created_graph, None)

with c3:
    st.graphviz_chart(dot_element)

if graph_name and maximum_clique:
    download_graph_button = c4.button("Télécharger graphe", 
                                        on_click=download_graph, 
                                        args=(graph_name, len(maximum_clique), dot_element, 1))
    
st.write(f"### La clique maximale : {maximum_clique}")

#--------------------------- Fonctions pour la création aléatoire de graphes -------------------------------

def generate_random_graph(vertices, edges):

    # Initialize the graph dictionary
    graph_dict = {i: [] for i in range(1, vertices + 1)}

    # Create edges randomly while avoiding duplicates and self-loops
    while edges > 0:
        vertex1 = randint(1, vertices)
        vertex2 = randint(1, vertices)
        if vertex1 != vertex2 and vertex2 not in graph_dict[vertex1]:
            graph_dict[vertex1].append(vertex2)
            graph_dict[vertex2].append(vertex1)
            edges -= 1

    graph_dict = dict(sorted(graph_dict.items()))
    st.session_state.random_created_graph = graph_dict

#------------------------------------ Création aléatoire de graphes ----------------------------------------

st.header("")
st.markdown("## Créer un graphe aléatoirement")

c1, c2 = st.columns([7,3])

with c2:
    animate("Components/algo_animation.json", 300, 300)

with c1:
    random_graph_name = st.text_input("Entrez le nom du graphe : ", key="random_graph_name")
    vertice_number, edges_number = display_random_graph_settings(random_graph_name)

if random_graph_name and vertice_number and edges_number:

        directory = st.session_state.working_directory + "\Graphes\Random\Images"
        filepath = os.path.join(directory,random_graph_name + ".png")

        if not os.path.exists(filepath):
            generate_random_graph(vertice_number, edges_number)
            maximum_clique, _ = maximum_clique_finder(st.session_state.random_created_graph, 1500, 0.99, 1000, None)
            dot_element = draw_graph(st.session_state.random_created_graph, None)
            st.graphviz_chart(dot_element)
            st.write(f"### La clique maximale : {maximum_clique}")
            download_graph(random_graph_name, len(maximum_clique), dot_element, 2)
        else:
            st.toast("Nom de graphe déjà pris", icon="❌")
