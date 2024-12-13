import random

champ_list=['Postać 1', 'Postać 2','Postać 3']

class solution:
    def __init__(self,list,champ_idx):
        self.list=list
        self.champ=champ_list[champ_idx]
    def __str__(self):
        return (f"Kolejność wierzchołków: {self.list}, Postać: {self.champ}")
    
    

    
class Champion:
    def __init__(self, name, camp_mod, travel_mod ):
        self.name= name
        self.camp_mod=camp_mod
        #self.current_camp_mod=camp_mod[0]
        self.travel_mod=travel_mod
        #self.current_travle_mod=travel_mod[0]
        self.lvl=1
        self.camps_done=0
        self.camps_required=[1,3,6,12,24]


    def zdobycie_celu(self):
        self.camps_done+=1
        if self.camps_done>=self.camps_required[self.lvl-1]:
            self.lvl+=1
            
    def __str__(self):
        """
        Reprezentacja tekstowa postaci.
        """
        return (f"Postać: {self.name}, Poziom: {self.lvl}, "
                f"Ilość celów: {self.camps_done}, "
                f"Modyfikator przemieszczania: {self.travel_mod}, "
                f"Modyfikator zdobywania: {self.camp_mod}")

class Mapa:
    def __init__(self, matrix,available_start_nodes, available_end_nodes, camp_cost):

        #Inicjalizuje mapy.
        self.mat = matrix
        self.nodes_count = len(matrix)
        self.start_nodes=available_start_nodes
        self.end_nodes=available_end_nodes
        self.camp_cost=camp_cost
        if camp_cost !=self.nodes_count:
            raise ValueError(" Mapa niepoprawna, lista kosztów celów jest krótsza od ilości celów")
        

    def odleglosc(self, node1, node2):
  
        #Zwraca odległość między dwoma wierzchołkami na podstawie macierzy sąsiedztwa.

        if 0 <= node1 < self.nodes_count and 0 <= node2 < self.nodes_count:
            return self.mat[node1][node2]
        else:
            raise ValueError(f"Wierzchołki muszą być w zakresie od 0 do liczba_wierzcholkow - 1. Obecna liczba wierzchołków: {self.nodes_count}")

    def wyswietl_macierz(self):
        #Wyświetla macierz sąsiedztwa w czytelny sposób.

        print("Macierz sąsiedztwa:")
        for wiersz in self.mat:
            print(wiersz)     
    def random_solution(self, champ_list):
        ch_op=len(champ_list)
        n=self.nodes_count
        if n <= 0:
            raise ValueError("n musi być liczbą całkowitą większą od zera.")
        lista = list(range(0, n ))
        random.shuffle(lista)
        champ=random.randint(0,ch_op-1)
        return solution(lista, champ)
    def objective_fun(self, sol, champ):
        if isinstance(sol, solution) and isinstance(champ,Champion ):
            lista=sol.list
            total_cost=0
        else:
            raise ValueError("Argument sol nie jest rozwiązaniem, jeżeli jest to lista, wybierz lub wylosuj postać i stwórz rozwiązanie")
        for i in range(len(lista)-1):
            total_cost+= self.odleglosc(lista[i],lista[i+1])*champ.travel_mod[champ.lvl-1]
            total_cost += champ.camp_mod[champ.lvl - 1]*self.camp_cost[lista[i]]
            champ.zdobycie_celu()
        total_cost+=champ.camp_mod[champ.lvl - 1]*self.camp_cost[lista[i+1]]


'''
Do implementacji:   Losowanie rozwiązania
                    Modyfikowanie rozwiązania (otoczenia)
                    Funkcja celu
'''

#tworzymy macierz dla danego przykłądu i zbioru wierzchołków dostępnych na początku
m1=[[100,5,5,14,16,12],[5,100,7,16,25,16],[5,7,100,12,16,14],[14,16,12,100,7,5],[16,25,16,7,100,5],[12,16,14,5,5,100]]
nodes=[1,2,3,4]
nodes_time=[x+15 for x in nodes]
d_start=[1,3,4,6]

def main():
    # Przykładowa macierz sąsiedztwa (0 oznacza brak połączenia)
    # funkcja kary -> zastopienie 0 dużą wartością
    macierz = [
        [0, 5, 0, 10],
        [5, 0, 3, 0],
        [0, 3, 0, 1],
        [10, 0, 1, 0]
    ]


    mapa = Mapa(macierz, d_start, d_start,nodes_time)
    # Sprawdzenie odległości między wierzchołkami
    print("Odległość między wierzchołkiem 0 a 1:", mapa.odleglosc(0, 1))
    print("Odległość między wierzchołkiem 2 a 3:", mapa.odleglosc(2, 3))
    # Wyświetlenie macierzy sąsiedztwa
    mapa.wyswietl_macierz()
    print(mapa.random_solution(champ_list))
    # Obsługa błędu dla niepoprawnych indeksów
    try:
        print("Odległość między wierzchołkiem 0 a 4:", mapa.odleglosc(0, 4))
    except ValueError as e:
        print("Błąd:", e)

main()

#mod_p_move=1#stworzenie listy od jeden do 18 takiej że wartości przyjmowane są rozłożone od 1 do 0.8
#mod_p_camp=1#stworzenie listy od jeden do 18 takiej że wartości przyjmowane są rozłożone od 1 do 0.5


#symulacja->losowanie rozwiązania, obliczanie funkcji celu dla tego rozwiązania
#first_node_index radnom number z przedziału 1 do 4
#first_node=d_start[first_node_index]
#nodes pop 
#for i in nodes:#stworzenie lsowej permutacji
#zbyt częste wykonywanie tego ruchu -> kara
#algorytm ewolucyjny???