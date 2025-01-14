import random
import numpy as np


def generate_map(n):
    A = np.random.rand(n, n)*35 # Generowanie losowej macierzy
    symmetric_matrix = (A + A.T) / 2  # Symetryzacja
    np.fill_diagonal(symmetric_matrix, 100)
    nodes=np.arange(n)
    nodes_cost=(np.random.rand(n)*10)+10
    return symmetric_matrix, nodes_cost

def generate_unique_numbers(x, a, b):
  if x > b - a + 1:
    raise ValueError("Zbyt wiele liczb do wygenerowania dla danego zakresu.")

  numbers = set()
  while len(numbers) < x:
    numbers.add(random.randint(a, b))
  return list(numbers)


# Klasa reprezentująca postać w grze
camps_required = [1, 3, 6, 12, 24]
class Champion:
    def __init__(self, name, camp_mod, travel_mod):
        self.name = name  # Nazwa postaci
        self.camp_mod = camp_mod  # Modyfikator zdobywania celów
        self.travel_mod = travel_mod  # Modyfikator kosztu podróży
        self.lvl = 1  # Początkowy poziom postaci
        self.camps_done = 0  # Liczba zrealizowanych celów
        self.camps_required = [1, 3, 6, 12, 24]  # Ilość celi wymaganych by awansować na dany poziom
        #5 wartośći camps required oznacza to że zaczynajac od poziomu pierwszego maksymalny to 6

    def zdobycie_celu(self):
        # Zwiększa liczbę zdobytych celów i aktualizuje poziom, jeśli wymagania są spełnione
        self.camps_done += 1
        if self.lvl<=len(camps_required):
            if self.camps_done >= self.camps_required[self.lvl - 1]:
                self.lvl += 1
    
    def reset(self):
        self.lvl=1
        self.camps_done=0

    def __str__(self):
        # Tekstowa reprezentacja postaci
        return (f"Postać: {self.name}\nPoziom: {self.lvl} \nIlość celów: {self.camps_done}")

# Lista przykładowych postaci
champ1=Champion('Kha\'Zix',[0.98,0.97,0.95,0.93,0.9,0.8,0.78],[1,1,0.8,0.8,0.8,0.8,0.8])
champ2=Champion('Wukong',[1,0.99,0.97,0.95,0.9,0.9,0.85],[0.9,0.9,0.8,0.8,0.8,0.8,0.8])
champ3=Champion('Gragas',[0.99,0.98,0.95,0.92,0.85,0.85,0.83],[1,1,0.85,0.85,0.85,0.85,0.85])
champ_list1 = [champ1, champ2, champ3]

# Klasa reprezentująca rozwiązanie (trasę i wybraną postać)
class solution:
    def __init__(self, list, champ_idx, lvl=0, time=None):
        self.list = list  # Lista wierzchołków, które tworzą trasę
        self.champ = champ_list1[champ_idx]  # Wybrana postać z listy
        self.champ_name=champ_list1[champ_idx].name
        self.camps_done=len(list)
        self.lvl_after=lvl
        self.time=time
    def __str__(self):
        # Tekstowa reprezentacja rozwiązania
        return (f"Kolejność wierzchołków: {self.list}\nPostać: {self.champ_name}")
    def __repr__(self): 
        return f"\n{self.champ_name}, {self.list}, {self.lvl_after}, {self.time}"

# Klasa reprezentująca mapę gry
class Mapa:
    def __init__(self, matrix, available_start_nodes, available_end_nodes, camp_cost):
        # Inicjalizuje mapę z macierzą odległości, dostępnymi wierzchołkami startowymi i końcowymi oraz kosztami celów
        self.mat = matrix
        self.nodes_count = len(matrix)  # Liczba wierzchołków
        self.start_nodes = available_start_nodes
        self.end_nodes = available_end_nodes
        self.camp_cost = camp_cost
        if len(camp_cost) != self.nodes_count:
            raise ValueError("Mapa niepoprawna, lista kosztów celów jest inna niż ilość celów")

    def odleglosc(self, node1, node2):
        # Zwraca odległość między dwoma wierzchołkami na podstawie macierzy sąsiedztwa
        if 0 <= node1 < self.nodes_count and 0 <= node2 < self.nodes_count:
            return self.mat[node1][node2]
        else:
            raise ValueError(f"Wierzchołki muszą być w zakresie od 0 do liczba_wierzcholkow - 1. Obecna liczba wierzchołków: {self.nodes_count}")

    def wyswietl_macierz(self):
        # Wyświetla macierz sąsiedztwa w czytelny sposób
        print("Macierz sąsiedztwa:")
        for wiersz in self.mat:
            print(wiersz)

    def random_solution(self, champ_list):
        # Tworzy losowe rozwiązanie z losową permutacją wierzchołków i postaci
        ch_op = len(champ_list)
        n = self.nodes_count
        if n <= 0:
            raise ValueError("n musi być liczbą całkowitą większą od zera.")
        lista = list(range(0, n))  # Lista wierzchołków
        random.shuffle(lista)  # Losowe przetasowanie wierzchołków
        champ = random.randint(0, ch_op - 1)  # Losowy indeks postaci
        return solution(lista, champ)

    def objective_fun(self, sol, champ):
        # Oblicza funkcję celu na podstawie rozwiązania i modyfikatorów postaci
        if isinstance(sol, solution) and isinstance(champ, Champion):
            lista = sol.list
            total_cost = 0
        else:
            raise ValueError("Argument sol (solution) nie jest rozwiązaniem, jeżeli jest to lista, wybierz lub wylosuj postać i stwórz rozwiązanie")
        champ.zdobycie_celu()
        total_cost+=champ.camp_mod[0]*self.camp_cost[lista[0]]
        for i in range(len(lista) - 1):
            # Koszt podróży
            total_cost += self.odleglosc(lista[i], lista[i + 1]) * champ.travel_mod[champ.lvl - 1]
            # Koszt zdobywania celu
            total_cost += champ.camp_mod[champ.lvl - 1] * self.camp_cost[lista[i]]
            champ.zdobycie_celu()
        # Dodanie kosztu dla ostatniego celu
        total_cost += champ.camp_mod[champ.lvl - 1] * self.camp_cost[lista[i + 1]]
        #print(f"Kolejność celów: {sol.list}\nPostać po przejsciu tych celów:\n{champ} ")
        if lista[0] not in self.start_nodes or lista[-1] not in self.end_nodes:
            #nakładanie funkcji kary dla wierzchołków które nie znajduja się 
            #w zbiorze wierzchołków początkowych lub końcowych
            total_cost+=100*self.nodes_count

        total_cost=round(total_cost,2)
        sol.lvl_after=champ.lvl
        sol.time=total_cost
        champ.reset()
        return total_cost
    def __str__(self):
        self.wyswietl_macierz()
        return f"Ilość celów: {self.nodes_count}, wierzchołki początkowe: {self.start_nodes}, wierzchołki końcowe: {self.end_nodes}"






def mutate(solution, mutation_type):
    #mutation_type = random.choice(["inversion", "swap", "champion"])
    
    if mutation_type == "inversion":
        # Mutacja inwersji
        size = len(solution.list)
        start, end = sorted(random.sample(range(size), 2))
        solution.list[start:end] = reversed(solution.list[start:end])
    
    elif mutation_type == "swap":
        # Mutacja przestawienia
        i, j = random.sample(range(len(solution.list)), 2)
        solution.list[i], solution.list[j] = solution.list[j], solution.list[i]
    
    elif mutation_type == "champion":
        # Mutacja zmiany postaci
        new_champ_idx = random.choice(range(len(champ_list1)))
        solution.champ = champ_list1[new_champ_idx]

def cycle_crossover(parent1, parent2):
    size = len(parent1.list)
    
    # Tworzenie cykli
    child_list = [-1] * size
    cycles = [0] * size
    current_cycle = 1
    
    for i in range(size):
        if cycles[i] == 0:  # Nowy cykl
            val = parent1.list[i]
            while cycles[i] == 0:
                cycles[i] = current_cycle
                i = parent1.list.index(parent2.list[i])
                val = parent1.list[i]
            current_cycle += 1
    
    # Tworzenie dziecka na podstawie cykli
    for i in range(size):
        if cycles[i] % 2 == 1:
            child_list[i] = parent1.list[i]
        else:
            child_list[i] = parent2.list[i]
    
    # Losowanie postaci od jednego z rodziców
    champ = random.choice([parent1.champ, parent2.champ])
    return solution(child_list, champ_list1.index(champ))

def order_crossover(parent1, parent2):
    size = len(parent1.list)
    start, end = sorted(random.sample(range(size), 2))
    
    # Dziecko początkowo puste (-1)
    child_list = [-1] * size
    
    # Skopiowanie segmentu od parent1
    child_list[start:end] = parent1.list[start:end]
    
    # Wypełnienie pozostałych pozycji z parent2
    parent2_values = [val for val in parent2.list if val not in child_list]
    idx = 0
    for i in range(size):
        if child_list[i] == -1:
            child_list[i] = parent2_values[idx]
            idx += 1
    
    # Losowanie postaci od jednego z rodziców
    champ = random.choice([parent1.champ, parent2.champ])
    return solution(child_list, champ_list1.index(champ))

def pmx_crossover(parent1, parent2):
    size = len(parent1.list)
    start, end = sorted(random.sample(range(size), 2))

    # Inicjalizacja dziecka
    child_list = [-1] * size

    # 1. Skopiowanie fragmentu z parent1
    child_list[start:end] = parent1.list[start:end]

    # 2. Wypełnienie pozostałych miejsc w dziecku
    mapping = {}  # Słownik do śledzenia mapowania genów
    for i in range(start, end):
        mapping[parent1.list[i]] = parent2.list[i]

    for i in range(size):
        if child_list[i] == -1:
            value = parent2.list[i]
            while value in mapping:
                value = mapping[value]
            child_list[i] = value

    # Utworzenie obiektu potomka
    # 4. Sprawdzenie poprawności rozwiązania
    if len(set(child_list)) != size or -1 in child_list:
        raise ValueError("PMX crossover failed: duplicate or missing elements.")

    # Wybierz champa losowo z rodziców
    champ = random.choice([parent1.champ, parent2.champ])
    return solution(child_list, champ_list1.index(champ))






def genetic_algorithm(map_obj, champ_list, x, y, z, crossover_type, mutation_type):
    """
    Algorytm genetyczny dla problemu optymalizacji.
    
    Args:
        map_obj (Mapa): Obiekt reprezentujący mapę.
        champ_list (list): Lista dostępnych postaci.
        x (int): Liczba losowych rozwiązań w początkowej populacji.
        y (int): Procent rozwiązań poddawanych mutacji (0 <= y <= 100).
        z (int): Liczba iteracji (pokoleń) algorytmu.
        crossover_type (str): Typ krzyżowania ('pmx', 'cycle', 'order').
        
    Returns:
        list: Lista najlepszych rozwiązań z każdego pokolenia.
        tuple: Najlepsze rozwiązanie ogółem (solution, czas).
    """
    
    
    def crossover(parent1, parent2, crossover_type):
        """Wybór odpowiedniego typu krzyżowania."""
        if crossover_type == 'pmx':
            return pmx_crossover(parent1, parent2)
        elif crossover_type == 'cycle':
            return cycle_crossover(parent1, parent2)
        elif crossover_type == 'order':
            return order_crossover(parent1, parent2)
        else:
            raise ValueError("Nieznany typ krzyżowania. Dostępne: 'pmx', 'cycle', 'order'.")

    # Początkowe generowanie populacji
    population = [map_obj.random_solution(champ_list) for _ in range(x)]
    best_solutions = []  # Lista najlepszych rozwiązań w każdym pokoleniu
    
    for _ in range(z):
        iter=_
        # Obliczanie czasu dla każdej osoby w populacji
        ranked_population = []
        for sol in population:
            sol_time = map_obj.objective_fun(sol, sol.champ)  # Wywołanie objective_fun
            ranked_population.append((sol, sol_time))
            
        
        # Posortowanie populacji względem czasu
        ranked_population.sort(key=lambda x: x[1])
        
        # Zapis najlepszego rozwiązania z populacji
        best_solution = ranked_population[0]
        best_solutions.append(best_solution)
        
        # Tworzenie nowej populacji przez krzyżowanie najlepszych rozwiązań
        new_population = []
        ranking_weights = [1 / (i + 1) for i in range(len(ranked_population))]  # Mniejsze indeksy mają większą wagę
        total_weight = sum(ranking_weights)

        for _ in range(len(ranked_population) // 2):
            # Losowanie rodziców z uwzględnieniem wag
            parent1 = random.choices([individual[0] for individual in ranked_population], weights=ranking_weights, k=1)[0]
            parent2 = random.choices([individual[0] for individual in ranked_population], weights=ranking_weights, k=1)[0]
            
            # Krzyżowanie
            child1 = crossover(parent1, parent2, crossover_type)
            child2 = crossover(parent2, parent1, crossover_type)
            
            # Dodawanie dzieci do nowej populacji
            new_population.append(child1)
            new_population.append(child2)
        
        # Mutacja określonego procenta populacji
        mutation_count = int(len(new_population) * y / 100)
        for _ in range(mutation_count):
            sol_to_mutate = random.choice(new_population)
            mutate(sol_to_mutate, mutation_type)
        
        # Uzupełnienie populacji o nowe losowe rozwiązania (jeśli populacja jest zbyt mała)
        max_attempts = 1000
        attempts = 0
        while len(new_population) < x and attempts < max_attempts:
            try:
                new_population.append(map_obj.random_solution(champ_list))
            except Exception as e:
                attempts += 1
                print(f"Błąd przy generowaniu losowego rozwiązania: {e}")
        if attempts == max_attempts:
            raise RuntimeError("Nie można wygenerować pełnej populacji.")

        
        population = new_population

    # Wybranie najlepszego rozwiązania ogółem
    overall_best = min(best_solutions, key=lambda x: x[1])
    only_solutions=[]
    for sol in best_solutions:
        only_solutions.append(sol[0])
    return only_solutions, overall_best

