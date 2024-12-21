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

    def __str__(self):
        # Tekstowa reprezentacja rozwiązania
        return (f"Kolejność wierzchołków: {self.list}\n{self.champ}")

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
        print(f"Kolejność celów: {sol.list}\nPostać po przejsciu tych celów:\n{champ} ")
        if lista[1] not in self.start_nodes or lista[-1] not in self.end_nodes:
            #nakładanie funkcji kary dla wierzchołków które nie znajduja się 
            #w zbiorze wierzchołków początkowych lub końcowych
            total_cost+=100
        total_cost=round(total_cost,2)

        return total_cost
    def __str__(self):
        self.wyswietl_macierz()
        return f"Ilość celów: {self.nodes_count}, wierzchołki początkowe: {self.start_nodes}, wierzchołki końcowe: {self.end_nodes}"


# Tworzymy przykładowe dane dla mapy i celów
m1 = [[100, 5, 5, 14, 16, 12],
      [5, 100, 7, 16, 25, 16],
      [5, 7, 100, 12, 16, 14],
      [14, 16, 12, 100, 7, 5],
      [16, 25, 16, 7, 100, 5],
      [12, 16, 14, 5, 5, 100]]
nodes = [0,1, 2, 3, 4, 5]
nodes_time = [x + 15 for x in nodes]  # Koszt każdego celu
d_start = [1, 3, 4, 6]  # Dostępne wierzchołki startowe
map1=Mapa(m1,d_start,d_start, nodes_time)
curr_sol_time=200
curr_sol=None
for i in range(10):

    sol_loop=map1.random_solution(champ_list1)
    sol_time=map1.objective_fun(sol_loop,sol_loop.champ)
    print(f'Wartość funkcji celu: {sol_time}\n')
    if sol_time<curr_sol_time:
        curr_sol_time=sol_time
        curr_sol=sol_loop
    sol_loop.champ.reset()
if curr_sol != None:
    print("Najlepsze rozwiązanie z 10 losowych:")
    new_sol=map1.objective_fun(curr_sol,curr_sol.champ)
    print(f'Czas: {new_sol}')
else:
    print('Nie wylosowana rozwiazania które jest poprawne')




#Stworzenie algoroytmu ewlucyjnego:
#Badanie populacji
#Meroda selekcji
#sąsiedztwo
#przebieg algorytmu
#nakład obliczeniowy
#21/22 stycznia?? kolokwium


#Działanie algorytmu -> Losowanie paru rozwiazań ()