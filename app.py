import streamlit as st
import constants as cst
import dimacs
from operation3 import display_op3
from settings import display_SA_settings, display_GA_settings, display_ACO_settings
from results import run
from fonctions import load_local_graphs, path_checker, sort_list, animate

st.set_page_config(page_title="App", page_icon="logo.png", layout="wide")

# Variables session state

# contiendera tous les graphes du workspace
st.session_state["local_graphs"] = load_local_graphs()

if "created_graph" not in st.session_state:
    st.session_state["created_graph"] = {}

if "random_created_graph" not in st.session_state:
    st.session_state["random_created_graph"] = {}

if "working_directory" not in st.session_state:
    st.session_state["working_directory"] = cst.working_directory_path

# Variables
local_graph_names_list = [graph.name for graph in st.session_state.local_graphs]
graph_dic = {}
benchmark_list = []
local_graph_list = []
timer = None

c1, c2 = st.columns([7,3])

with c2:
    animate("Components/data_animation.json", 300, 300)

c1.title("Bienvenue")

# Choix de l'opération
c1.header("Que voulez vous faire ?")
operation = c1.selectbox("Veuillez choisir une opération", cst.operations, label_visibility="collapsed")

if operation == cst.operations[2]: # Déterminer La clique maximal relié à un nœud
    graph_dic = display_op3()
    
else:

    c1, c2 = st.columns([7,3])

    with c2:
        animate("Components/graph_animation.json", 250, 250)
    
    c1.header("Sur quel graphe ?")

    benchmark_name_list = c1.multiselect("Benchmarks", 
                                    dimacs.graph_names_list, 
                                    placeholder="Sélectionnez un ou plusieurs graphes")
    benchmark_list = [graph for graph in dimacs.graph_list if graph.name in benchmark_name_list]
    
    local_graph_name_list = c1.multiselect("Graphe locale",
                                    local_graph_names_list, 
                                    placeholder="Sélectionnez un ou plusieurs graphes")
    local_graph_list = [graph for graph in st.session_state.local_graphs if graph.name in local_graph_name_list]

graph_list = benchmark_list + local_graph_list


# Choix du ou des algos à appliqués

st.header("")
st.header("Avec quel algorithme ?")
algo_list = st.multiselect("_", 
                            cst.algorithms, 
                            label_visibility="collapsed",
                            placeholder="Veuillez choisir la ou les métaheuristiques à appliquer")
algo_list = sort_list(algo_list)

# Paramètres
SA_settings = None
GA_settings = None
ACO_settings = None

# Afficher les paramètres des algorithmes seléctionnés selon l'opération choisis

option = 2 if operation == cst.operations[1] else 1

if cst.algorithms[0] in algo_list: # Recuit simulé
    SA_settings = display_SA_settings(option)

if cst.algorithms[1] in algo_list: # Algorithme génétique
    GA_settings = display_GA_settings(option)

if cst.algorithms[2] in algo_list: # Colonies de fourmis
    ACO_settings = display_ACO_settings(option)

# Paramètres optionnels

st.header("")
c1, c2 = st.columns([7,3])

c1.header("Définir une limite de temps ?")
c3, c4 = c1.columns([1,9])

toggler = c3.toggle("?", label_visibility="hidden")
timer = c4.slider(label="Temps en secondes", value=30, min_value=1, max_value=300, label_visibility="collapsed") if toggler else None

c1.header("Modifier l'espace de travail ?")
c3, c4 = c1.columns([1,9])

toggler = c3.toggle("Modifier", label_visibility="hidden")
path = c4.text_input(label=",", label_visibility="collapsed", placeholder=st.session_state.working_directory) if toggler else None

if path and path_checker(path):
    st.session_state.working_directory = path
     
with c2:
    animate("Components/settings_animation.json", 300, 300)

# Vérifier que tout est bon avant de lancer les calculs
if operation and algo_list and (graph_list or graph_dic) and (SA_settings or GA_settings or ACO_settings):
    
    graph_data = None

    if graph_list:
        graph_data = graph_list
    
    elif graph_dic:
        graph_data = graph_dic
    
    params = (operation, graph_data, algo_list, SA_settings, GA_settings, ACO_settings, timer)
    run_button = st.button("Valider", key="run_button")
    
    if run_button:
        run(*params)
