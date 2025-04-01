import random
import time

def initialize_pheromones(graph, initial_pheromone):
    pheromones = {v: initial_pheromone for v in graph}
    return pheromones

def update_pheromones(pheromones, cliques, decay_rate, reward):
    for v in pheromones.keys():
        pheromones[v] *= (1 - decay_rate)  # decay existing pheromone
    for clique in cliques:
        for v in clique:
            if v in pheromones:
                pheromones[v] += reward / len(clique)  # reward based on clique size
    return pheromones

def select_vertex(graph, pheromones, current_clique):
    
    candidates = [v for v in graph if all(v in graph[neigh] for neigh in current_clique)]
    if not candidates:
        return None
    
    probabilities = [pheromones[v]**2 / (1 + len(graph[v])) for v in candidates]  # squared pheromone value and normalized by degree
    total = sum(probabilities)
    if total > 0:
        probabilities = [p / total for p in probabilities]
        return random.choices(candidates, weights=probabilities, k=1)[0]
    return random.choice(candidates)

def construct_clique(graph, pheromones, max_iterations):
    current_clique = [random.choice(list(graph.keys()))]
    for _ in range(max_iterations):
        v = select_vertex(graph, pheromones, current_clique)
        if not v:
            break
        current_clique.append(v)
    return current_clique

def fitness(clique):
    return len(clique)

#--------------------------------------------------------------------------------------------------

def maximum_clique_finder(graph, nb_ants, initial_pheromone, decay_rate, reward, nb_iterations, timer):
    
    pheromones = initialize_pheromones(graph, initial_pheromone)
    best_clique = []
    start_time = time.time()

    for _ in range(nb_iterations):
        cliques = [construct_clique(graph, pheromones, 20) for _ in range(nb_ants)]
        best_clique = max(cliques, key=len, default=best_clique)
        pheromones = update_pheromones(pheromones, cliques, decay_rate, reward)
        
        if timer and time.time() - start_time > timer:
              break
                  
    end_time = time.time()
    calcul_time = round(end_time - start_time, 2)

    return sorted(best_clique), calcul_time

#--------------------------------------------------------------------------------------------------

def all_clique_finder(graph, nb_ants, initial_pheromone, decay_rate, reward, nb_iterations, timer):
    
    pheromones = initialize_pheromones(graph, initial_pheromone)
    all_cliques = set()
    start_time = time.time()

    for _ in range(nb_iterations):
        cliques = [construct_clique(graph, pheromones, 20) for _ in range(nb_ants)]
        
        for clique in cliques:
            new_clique = tuple(sorted(clique))
            if new_clique not in all_cliques and fitness(clique) > 1:
                all_cliques.add(new_clique)

        update_pheromones(pheromones, cliques, decay_rate, reward)

        if timer and (time.time() - start_time > timer):
            break

    end_time = time.time()
    calcul_time = round(end_time - start_time, 2)
    
    all_cliques.discard(())
    return sorted(all_cliques, key=len), calcul_time

#--------------------------------------------------------------------------------------------------

def check_vertex(clique, vertex, graph):
    return all(vertex in graph[neigh] for neigh in clique)

def select_next_vertex(pheromones, graph, current_clique):
    candidates = [v for v in graph if v not in current_clique and check_vertex(current_clique, v, graph)]
    if not candidates:
        return None
    probabilities = [pheromones[v] for v in candidates]
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    return random.choices(candidates, weights=probabilities, k=1)[0]

def construct_clique_from_vertex(graph, pheromones, max_iterations, initial_vertex):
    current_clique = [initial_vertex]
    for _ in range(max_iterations):
        v = select_vertex(graph, pheromones, current_clique)
        if not v:
            break
        current_clique.append(v)
    return set(current_clique)

#--------------------------------------------------------------------------------------------------

def vertex_maximum_clique_finder(graph, initial_vertex, nb_ants, initial_pheromone, reward, decay_rate, nb_iterations, timer):
    pheromones = initialize_pheromones(graph, initial_pheromone)
    best_clique = set([initial_vertex])
    start_time = time.time()

    for _ in range(nb_iterations):
        cliques = [construct_clique_from_vertex(graph, pheromones, 20, initial_vertex) for _ in range(nb_ants)]
        current_best = max(cliques, key=len)
        if len(current_best) > len(best_clique):
            best_clique = current_best

        update_pheromones(pheromones, cliques, reward, decay_rate)
        
        if timer and (time.time() - start_time > timer):
            break

    end_time = time.time()
    calcul_time = round(end_time - start_time, 2)

    return sorted(best_clique), calcul_time
