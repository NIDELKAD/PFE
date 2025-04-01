import streamlit as st
import constants as cst
from streamlit_lottie import st_lottie
from collections import Counter
import dimacs, json, os, graphviz, csv, time, datetime
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px

# Fonction qui récupère tous les fichiers .json d'un répertoire 

def graphs_getter(path):

    graph_list = []

    for filename in os.listdir(path):
        tempo_graph = {}

        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):

            with open(filepath, "r") as file:
                graph_object = json.load(file)

            # convertir les clés du graph_dict en int car elle sont string à cause de json.dump()
            for k, v in graph_object['graph_dic'].items():
                tempo_graph[int(k)] = v
            graph_object['graph_dic'] = tempo_graph

            graph_list.append(graph_object)

    return graph_list

# fontion qui charge tous les les graphes qui se trouvent dans le Workspace

def load_local_graphs():
    
    # Liste qui va contenir les graphes locaux
    local_graphs = []
    manual_graph_list = []
    random_graph_list = []

    # Charger les grahpes locaux
    manual_graph_list = graphs_getter(cst.manual_json_path)
    random_graph_list = graphs_getter(cst.random_json_path)

    # Fusioner les 2 listes
    graph_list = manual_graph_list + random_graph_list

    # Créer l'objet Graph
    for graph in graph_list:

        new_graph = dimacs.Graph(graph['name'], 
                                graph['nodes'], 
                                graph['edges'], 
                                graph['clique_size'], 
                                graph['graph_dic'],
                                None)
        
        local_graphs.append(new_graph)

    return local_graphs

# Fonction qui vérifie que le chemin passé en paramètre existe rééllement

def path_checker(path):

    if len(path) > 2 and (path[0] and ("C:", "D:", "F", "G") and path[1] == ":" and path[2] == "\\"):

        if os.path.exists(path):
            path_exists = True
        
        else:
            
            try:
                os.makedirs(path)
                path_exists = True
            
            except OSError as e:
                st.toast("Une erreur est survenue", icon="❌")
                return False
            
        if path_exists:
            
            if not os.path.exists(path+"/Graphes"):
                os.makedirs(path+"/Graphes")
            
            if not os.path.exists(path+"/Graphes/Manual"):
                os.makedirs(path+"/Graphes/Manual")
            
            if not os.path.exists(path+"/Graphes/Random"):
                os.makedirs(path+"/Graphes/Random")
            
            if not os.path.exists(path+"/Graphes/Manual/JSON"):
                os.makedirs(path+"/Graphes/Manual/JSON")
            
            if not os.path.exists(path+"/Graphes/Manual/Images"):
                os.makedirs(path+"/Graphes/Manual/Images")
            
            if not os.path.exists(path+"/Graphes/Random/JSON"):
                os.makedirs(path+"/Graphes/Random/JSON")
            
            if not os.path.exists(path+"/Graphes/Random/Images"):
                os.makedirs(path+"/Graphes/Random/Images")

            if not os.path.exists(path+"/Cliques"):
                os.makedirs(path+"/Cliques")

            st.toast("Espace de travail mise à jour", icon="✅")

            return True

    else:
        st.toast(f"Le chemin d'accès '{path}' est invalide", icon="❌")
        return False

# Fonction pour trier l'algo liste récupérer depuis le widget multiselect

def sort_list(algo_list):
    tempo_list = []
    for algo in cst.algorithms:
        if algo in algo_list:
            tempo_list.append(algo)
    return tempo_list     

# Fonction animation
@st.cache_resource(experimental_allow_widgets=True)
def animate(file_path, widget_height, widget_width):
    with open(file_path, 'r') as f:
        animation_data = json.load(f)
        st_lottie(animation_data, height=widget_height, width=widget_width)

# Fonction pour charger le dictionnaire du graphe associé

def get_graph_dic(graph):
    graph_dic = {}
    with open(graph.file_path, 'r') as f:
        for line in f:
            if line.startswith('e'):
                _, u, v = line.split()
                u, v = int(u), int(v)
                if u not in graph_dic:
                    graph_dic[u] = []
                if v not in graph_dic:
                    graph_dic[v] = []
                graph_dic[u].append(v)
                graph_dic[v].append(u)
    graph.graph_dic = graph_dic

# fonction pour charger les graphes sélectionnés
def load_graph_dic(graph_list):
    for graph in graph_list:
        if not graph.graph_dic:
            get_graph_dic(graph)

# Dessiner graphe
def draw_graph(graph_dict, vertex_to_color):
    dot = graphviz.Graph()  # Utiliser la classe Graph pour un graphe non orienté
    sorted_dict = {key: graph_dict[key] for key in sorted(graph_dict.keys())}

    for vertex, neighbors in sorted_dict.items():

        if vertex_to_color:
            
            if vertex != vertex_to_color:
                dot.node(str(vertex))
            else:
                node_style = {'color': 'red', 'style': 'filled'}
                dot.node(str(vertex), _attributes=node_style)
         
        if neighbors:

            for neighbor in neighbors:
                
                # Ajouter des arêtes seulement si le nœud actuel est plus petit que le voisin
                    if vertex < neighbor:
                        dot.edge(str(vertex), str(neighbor))
            
        else: # sommet isolé
            dot.node(str(vertex))

    return dot    

def create_graph_from_clique(clique):
    graph_dic = {}
    for i in clique:
        graph_dic[i] = [v for v in clique if v != i]
    return graph_dic

# ---------------------------------- fonctions operations 1  ----------------------------------

def operation1_display(clique, algo_list, clique_list, index):
    algo_name = cst.algorithms[index]
    algo_list.append(algo_name)
    clique_list.append(clique[0])
    st.write(f"## Résultat {algo_name}")
    st.markdown(f"### Clique trouvée : {clique[0]}")
    st.write("### Taille de la clique : ", len(clique[0]))
    st.write("### Temps de calcul : ", clique[1], "s")

# ---------------------------------- fonctions operations 2 ----------------------------------

def csv_file_generator(directory_name, algo_name, all_cliques):

    filename = algo_name + ".csv"
    filepath = os.path.join(directory_name, filename)
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for clique in all_cliques:
            writer.writerow(list(clique))

    st.toast("Fichier ajouté", icon="✅")

def create_pie_chart(all_cliques):

    # Récupérer un objet Counter qui contient un dictionnaire de (taille clique / occurence)
    clique_size_counts = Counter(len(clique) for clique in all_cliques)
    # Trier le dictionnaire dans l'ordre des tailles des cliques
    clique_size_counts = dict(sorted(clique_size_counts.items()))
    total_cliques = len(all_cliques)

    # Calculer les pourcentage de chaque taille de clique et les stockés dans un dictionnaire
    clique_size_percentages = {size: (count / total_cliques) * 100 for size, count in clique_size_counts.items()}

    # Créer un dictionanire qui contient les messages "Clique de taille = taille" pour chaque taille de clique
    size_ranges = {}
    for i in clique_size_counts:
        size_ranges[i] = f"Clique de taille = {i}"

    # Créer un dictionnaire finale de la forme (Clique de taille = taille : pourcentage) qui sera passé comme
    # paramètre à la fonction px.pie() qui crééra le diagramme circulaire (camembert)
    
    pie_dict = {
        "size" : [],
        "percentage" : [],
    }

    # Remplir le dictionnaire 
    for size, count in clique_size_percentages.items():
        if size in size_ranges:
            pie_dict["size"].append(size_ranges[size])
            pie_dict["percentage"].append(count)

    # Create the pie chart
    fig = px.pie(pie_dict, values="percentage", names="size", title="Clique Size Distribution")
    st.plotly_chart(fig, use_container_width=True)

def operation2_display(directory_name, all_cliques, algo_list, all_cliques_list, index):
    algo_name = cst.algorithms[index]
    algo_list.append(algo_name)
    all_cliques_list.append(all_cliques[0])
    st.write(f"## Résultat {algo_name}")
    st.write("### Nombre de cliques trouvées : ", len(all_cliques[0]))
    st.write("### Temps de calcul : ", all_cliques[1], "s")
    csv_file_generator(directory_name, algo_name, all_cliques[0])
    create_pie_chart(all_cliques[0])

# ---------------------------------- operations 3 functions ----------------------------------

def operation3_display(clique, vertex, algo_list, clique_list, index):
    algo_name = cst.algorithms[index]
    algo_list.append(algo_name)
    clique_list.append(clique[0])
    st.write(f"## Résultat {algo_name}")
    st.markdown(f"### La clique maximale relié à {vertex} : {clique[0]}")
    st.write("### Taille de la clique : ", len(clique[0]))
    st.write("### Temps de calcul : ", clique[1], "s")

# ---------------------------------- display results functions ----------------------------------

def operation1_results(graph, SA_clique, GA_clique, ACO_clique):

    algo_list = [] # contient les noms des algos appliqués
    clique_list = [] # contient les cliques trouvées par les différents algos
    
    if SA_clique: # Recuit simulé
        operation1_display(SA_clique, algo_list, clique_list, 0)
    
    if GA_clique: # Alogirhtme génétique
        operation1_display(GA_clique, algo_list, clique_list, 1)
    
    if ACO_clique: # Colonie de fourmis
        operation1_display(ACO_clique, algo_list, clique_list, 2)

    # Tableau récapitulatif

    # valeurs sur la colonne "Taille de la clique"
    clique_size_list = [len(clique) for clique in clique_list]
    
    # valeurs sur la colonne "Efficacité %"
    efficiency_list = [round(e/graph.clique_size*100, 2) for e in clique_size_list]

    # Création du DataFrame
    table_df = pd.DataFrame({
        "Algorithme": algo_list,
        "Clique trouvée": clique_list,
        "Taille de la clique": clique_size_list,
        "Clique maximale": [graph.clique_size] * len(clique_list),
        "Efficacité %" : efficiency_list
    })

    # Affichage du tableau
    st.write("## Tableau récapitulatif")
    AgGrid(table_df, fit_columns_on_grid_load=True, height=30*len(clique_list) + 30)

    # Représentation graphique

    clique_size_list = clique_size_list + [graph.clique_size] # Les barres sur le graphique
    algo_list = algo_list + ["Optimum global"] # Les noms des algos sur l'axe des abscisses

    chart_df = pd.DataFrame({
        "Algorithmes": algo_list,
        "Taille de la clique": clique_size_list
    })

    # Affichage du graphique
    st.write("## Représentation graphique")
    fig = px.bar(chart_df, x='Algorithmes', y='Taille de la clique')
    st.plotly_chart(fig, use_container_width=True)

    return efficiency_list

# ---------------------------------------------------------------------------------------------------

def operation2_results(graph, SA_clique, GA_clique, ACO_clique):

    algo_list = [] # contient les noms des algos appliqués
    all_clique_list = [] # contient les cliques calculés
    
    date_id = "\\" + datetime.date.today().strftime(r"%Y-%m-%d")
    current_time = time.localtime()
    time_id = "\\" + time.strftime("%H-%M-%S", current_time)
    directory_name = st.session_state.working_directory + "\Cliques" + date_id + time_id + graph.name
    os.makedirs(directory_name)

    if SA_clique: # Recuit simulé
        operation2_display(directory_name, SA_clique, algo_list, all_clique_list, 0)
    
    if GA_clique: # Alogirhtme génétique
        operation2_display(directory_name, GA_clique, algo_list, all_clique_list, 1)
    
    if ACO_clique: # Colonie de fourmis
        operation2_display(directory_name, ACO_clique, algo_list, all_clique_list, 2)

    all_clique_size_list = [len(clique) for clique in all_clique_list]

    # Représentation graphique si il y'a au moins 2 algos

    if len(algo_list) > 1:

        chart_df = pd.DataFrame({
            "Algorithmes": algo_list,
            "Nombre de cliques": all_clique_size_list
        })

        # Affichage du graphique
        st.write("## Représentation graphique")
        fig = px.bar(chart_df, x='Algorithmes', y='Nombre de cliques')
        st.plotly_chart(fig, use_container_width=True)

    return all_clique_size_list

# ----------------------------------------------------------------------------------------------------

def operation3_results(vertex, SA_clique, GA_clique, ACO_clique):

    algo_list = [] # contient les noms des algos appliqués
    clique_list = [] # contient les cliques calculés
    
    if SA_clique: # Recuit simulé
        operation3_display(SA_clique, vertex, algo_list, clique_list, 0)
    
    if GA_clique: # Alogirhtme génétique
        operation3_display(GA_clique, vertex, algo_list, clique_list, 1)
    
    if ACO_clique: # Colonie de fourmis
        operation3_display(ACO_clique, vertex, algo_list, clique_list, 2)

    clique_size_list = [len(clique) for clique in clique_list]

    # Représentation graphique

    if len(algo_list) > 1:

        chart_df = pd.DataFrame({
            "Algorithmes": algo_list,
            "Taille de la clique": clique_size_list
        })

        # Affichage du graphique
        st.write("## Représentation graphique")
        fig = px.bar(chart_df, x='Algorithmes', y='Taille de la clique')
        st.plotly_chart(fig, use_container_width=True)

    # Affichage des cliques (sous-graphes)

    for i , j in zip(clique_list, algo_list):
        st.write(f"## Clique trouvé par {j}")
        graph_dic = create_graph_from_clique(i)
        st.graphviz_chart(draw_graph(graph_dic, vertex), use_container_width=False)

    return clique_size_list

# Fonction qui affiche un graphique finale pour comparer entre les différents algorithmes

def display_comparison(graph_name_list, algo_list, result_list, operation):

    data = []
    
    if operation == cst.operations[0]:
        algo_string = "Efficacité"
        for graph_name in graph_name_list:
            data.append({"Graphes": graph_name, "Algorithmes": "Optimum global", algo_string: 100})

    elif operation == cst.operations[1]:
        algo_string = "Nombre de cliques"
    else:
        algo_string = "Taille de la clique maximale"
        
    for i, graph_name in enumerate(graph_name_list):
        for j, algo in enumerate(algo_list):
            data.append({"Graphes": graph_name, "Algorithmes": algo, algo_string: result_list[i][j]})

    line_chart_frame = pd.DataFrame(data)

    fig = px.line(line_chart_frame, x="Graphes", y=algo_string, color="Algorithmes", markers=True)
    st.plotly_chart(fig, use_container_width=True)
