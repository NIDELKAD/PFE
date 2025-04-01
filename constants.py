import streamlit as st

graphiz_bin_path = r"C:\Program Files (x86)\graphiz\bin"

working_directory_path = r"C:\Users\21356\AppData\Roaming\Python\Python310\site-packages\App_V5\Workspace"

if "working_directory" not in st.session_state:
    st.session_state["working_directory"] = working_directory_path

manual_json_path = st.session_state.working_directory + "\Graphes\Manual\JSON"

random_json_path = st.session_state.working_directory + "\Graphes\Random\JSON"

operations = [  "Trouver la clique maximale du graphe", 
                "Localiser toutes les cliques du graphe", 
                "Déterminer La clique maximal reliée à un sommet"
                ]

algorithms = ["Recuit simulé", "Algorithme génétique", "Colonies de fourmis"]
