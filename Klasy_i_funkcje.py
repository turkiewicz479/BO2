import random




# Klasa reprezentująca postać w grze
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
        if self.camps_done >= self.camps_required[self.lvl - 1]:
            self.lvl += 1
    def reset(self):
        self.lvl=1
        self.camps_done=0

    def __str__(self):
        # Tekstowa reprezentacja postaci
        return (f"Postać: {self.name}\nPoziom: {self.lvl} \nIlość celów: {self.camps_done}")

# Lista przykładowych postaci
champ1=Champion('Kha\'Zix',[0.98,0.97,0.95,0.93,0.9,0.8],[1,1,0.8,0.8,0.8,0.8])
champ2=Champion('Wukong',[1,0.99,0.97,0.95,0.9,0.9],[0.9,0.9,0.8,0.8,0.8,0.8])
champ3=Champion('Gragas',[0.99,0.98,0.95,0.92,0.85,0.85],[1,1,0.85,0.85,0.85,0.85])
champ_list1 = [champ1, champ2, champ3]

# Klasa reprezentująca rozwiązanie (trasę i wybraną postać)
class solution:
    def __init__(self, list, champ_idx):
        self.list = list  # Lista wierzchołków, które tworzą trasę
        self.champ = champ_list1[champ_idx]  # Wybrana postać z listy
        self.champ_name=champ_list1[champ_idx].name

    def __str__(self):
        # Tekstowa reprezentacja rozwiązania
        return (f"Kolejność wierzchołków: {self.list}\nPostać: {self.champ_name}")

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
            raise ValueError("Mapa niepoprawna, lista kosztów celów jest krótsza od ilości celów")

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
        if lista[1] not in self.start_nodes or lista[-1] not in self.end_nodes:
            #nakładanie funkcji kary dla wierzchołków które nie znajduja się 
            #w zbiorze wierzchołków początkowych lub końcowych
            total_cost+=100
        total_cost=round(total_cost,2)

        return total_cost
    def __str__(self):
        self.wyswietl_macierz()
        return f"Ilość celów: {self.nodes_count}, wierzchołki początkowe: {self.start_nodes}, wierzchołki końcowe: {self.end_nodes}"

def pmx_crossover(parent1, parent2):
    size = len(parent1.list)
    start, end = sorted(random.sample(range(size), 2))
    
    child_list = [-1] * size
    
    child_list[start:end] = parent1.list[start:end]
    
    for i in range(start, end):
        val = parent2.list[i]
        if val not in child_list:
            while val in child_list[start:end]:
                idx = parent1.list.index(val)
                val = parent2.list[idx]
            child_list[child_list.index(-1)] = val
    
    for i in range(size):
        if child_list[i] == -1:
            val = parent2.list[i]
            while val in child_list:
                idx = parent1.list.index(val)
                val = parent2.list[idx]
            child_list[i] = val
    
    champ = random.choice([parent1.champ, parent2.champ])
    return solution(child_list, champ_list1.index(champ))
def mutate(solution):
    mutation_type = random.choice(["inversion", "swap", "champion"])
    
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
