from Klasy_i_funkcje import *
import numpy as np

def test_genetic_algorithm(test_sample, map_size_list, start_nodes_size_list, end_nodes_size_list, 
                           mutation_types, crossover_types):
    with open("genetic_algorithm_results.txt", "w") as file:
        file.write(f"Wyniki testów dla test_sample = {test_sample}\n")
    
    for i in range(len(map_size_list)):
        map_size = map_size_list[i]
        d_start_size = int(start_nodes_size_list[i])
        d_end_size = int(end_nodes_size_list[i])
        print(f"Mapa o rozmiarze: {map_size}")
        with open("genetic_algorithm_results.txt", "a") as file:
            file.write(f"\n===\nRozmiar mapy: {map_size} wierzchołków\n===\n")

        d_start = generate_unique_numbers(d_start_size, 0, map_size - 1)
        d_end = generate_unique_numbers(d_end_size, 0, map_size - 1)
        matrix, nodes_time = generate_map(map_size)
        curr_map = Mapa(matrix, d_start, d_end, nodes_time)

        population_size_list = [100,200,500]
        numb_of_gen_list = [20, 50]
        mutation_chance_list = [20, 50]

        default_population_size = 100
        default_numb_of_gen = 10
        default_mutation_chance = 10


        for pop_size in population_size_list:
            test_params(curr_map, champ_list1, test_sample, pop_size, default_numb_of_gen, default_mutation_chance, 
                        crossover_types, mutation_types, "Rozmiar populacji", pop_size)

        for gen_num in numb_of_gen_list:
            test_params(curr_map, champ_list1, test_sample, default_population_size, gen_num, default_mutation_chance, 
                        crossover_types, mutation_types, "Liczba pokoleń", gen_num)

        for mut_chance in mutation_chance_list:
            test_params(curr_map, champ_list1, test_sample, default_population_size, default_numb_of_gen, mut_chance, 
                        crossover_types, mutation_types, "Szansa na mutacje", mut_chance)


def test_params(curr_map, champ_list1, test_sample, pop_size, gen_num, mut_chance, 
                crossover_types, mutation_types, param_name, param_value):
    """
    Pomocnicza funkcja testująca zestawy parametrów.
    """
    for crossover_type in crossover_types:
        for mutation_type in mutation_types:
            map_time_values = []

            for _ in range(test_sample):
                best_sol, list_of_sol = genetic_algorithm(curr_map, champ_list1, pop_size, 
                                                          mut_chance, gen_num,crossover_type, mutation_type)
                map_time_values.append(best_sol[0].time)

            mean_time = np.mean(map_time_values)
            std_dev_time = np.std(map_time_values)
            best_time = min(map_time_values)

            with open("genetic_algorithm_results.txt", "a") as file:
                file.write(f"\nParametry:\n")
                file.write(f"{param_name}: {param_value}, "
                           f"Typ krzyżowania: {crossover_type}, Typ mutacji: {mutation_type}\n")
                file.write(f"Otrzymane wyniki:\n")
                file.write(f"Wartość średnia: {mean_time:.2f}, "
                           f"Odchylenie standardowe: {std_dev_time:.2f}, "
                           f"Najlepszy wynik: {best_time:.2f}\n")

test_sample = 100
map_size_list = [10, 25, 50]
start_nodes_size_list = [x / 5 for x in map_size_list]
end_nodes_size_list = [x / 5 for x in map_size_list]
mutation_types = ["swap", "inversion", "champ"]
crossover_types = ["pmx", "cycle", "order"]

test_genetic_algorithm(test_sample, map_size_list, start_nodes_size_list, end_nodes_size_list, 
                       mutation_types, crossover_types)
print("Koniec testów")