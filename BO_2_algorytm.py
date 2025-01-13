from Klasy_i_funkcje import *
import tkinter as tk
class GeneticAlgorithmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja algorytmu genetycznego")

        # Etykiety i pola tekstowe dla parametrów
        self.map_size_label = tk.Label(self, text="Wielkość mapy:")
        self.map_size_entry = tk.Entry(self)
        self.d_start_size_label = tk.Label(self, text="Ilość wierzchołków startowych:")
        self.d_start_size_entry = tk.Entry(self)
        self.d_end_size_label = tk.Label(self, text="Ilość wierzchołków końcowych:")
        self.d_end_size_entry = tk.Entry(self)
        # ... pozostałe etykiety i pola dla d_start, d_end, itp.

        # Listy rozwijane dla krzyżowania i mutacji
        self.crossover_types = ["pmx","cycle", "order"]
        # ... podobnie dla mutacji
        self.mutate_types =["swap","inversion","champ",]

        # Przycisk do generowania mapy
        self.generate_map_button = tk.Button(self, text="Generuj mapę", command=self.generate_map)

        # Przycisk do uruchomienia algorytmu
        self.run_button = tk.Button(self, text="Uruchom algorytm", command=self.run_algorithm)

        # Umieszczenie elementów w oknie
        # ...

        # Funkcje obsługujące zdarzenia
    def generate_map(self):
        map_size = int(self.map_size_entry.get())
        d_start_size = int(self.d_start_size_entry.get())
        d_end_size = int(self.d_end_size_entry.get())
        # ... pobierz pozostałe wartości
        d_start = generate_unique_numbers(d_start_size,0,6)  
        d_end = generate_unique_numbers(d_end_size, 16,23)
        m2, nodes_time = generate_map(map_size)
        map2=Mapa(m2,d_start,d_end,nodes_time)
        # ... ustaw stan aplikacji po wygenerowaniu mapy

    def run_algorithm(self):
        # Pobierz wszystkie parametry z interfejsu
        # ...
        list_of_sol, best_sol = genetic_algorithm(map2, crossover_type, ...)
        # ... wyświetl wyniki

def main():

    d_start = generate_unique_numbers(4,0,6)  
    d_end = generate_unique_numbers(4, 16,23)
    m2, nodes_time=generate_map(25)
    map2=Mapa(m2,d_start,d_end,nodes_time)

    #Zakładamy że jeżeli przejscie wszystkich celów zajmie więcej niż 200 sekund 
    #to rozwizanie jest bardzo slabe i nie chcemy go zapisać




    #Generowanie x losowych rozwiązań, następnie stworzenie rankingu pod względem czasu rozwiązania. Następnie adekwatne krzyżowanie, rodzaj krzyżowania wybierany jako argument funkcji
    # następnie y procent rozwiązań jest mutowanych, y również jest argumentem funkcji, nastęnie kończymy ten etap i oceniamy dopsowanie (czas rozwiązań) znowu tworzymy ranking i powtarzamy poprzednie kroki, najlepsze rozwiązanie z każdego rankingu zostaje zapisane do listy potencjalnych rozwiązań

    list_of_sol, best_sol = genetic_algorithm(map2, champ_list1, 100,10,10, 'pmx', 'champ')
    #time=map1.objective_fun(best_sol)
    print(list_of_sol)
    print(best_sol)
    g=1
    pmx_crossover(list_of_sol[0], list_of_sol[1])
    
    #print(time, best_sol.champ)

main()



#Stworzenie algoroytmu ewlucyjnego:
#Badanie populacji
#Metoda selekcji
#sąsiedztwo
#przebieg algorytmu
#nakład obliczeniowy
#21/22 stycznia?? kolokwium


#Działanie algorytmu -> Losowanie paru rozwiazań ()