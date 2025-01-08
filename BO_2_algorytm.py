from Klasy_i_funkcje import *


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

#Zakładamy że jeżeli przejscie wszystkich celów zajmie więcej niż 200 sekund 
#to rozwizanie jest bardzo slabe i nie chcemy go zapisać




#Generowanie x losowych rozwiązań, następnie stworzenie rankingu pod względem czasu rozwiązania. Następnie adekwatne krzyżowanie, rodzaj krzyżowania wybierany jako argument funkcji
# następnie y procent rozwiązań jest mutowanych, y również jest argumentem funkcji, nastęnie kończymy ten etap i oceniamy dopsowanie (czas rozwiązań) znowu tworzymy ranking i powtarzamy poprzednie kroki, najlepsze rozwiązanie z każdego rankingu zostaje zapisane do listy potencjalnych rozwiązań

list_of_sol, best_sol = genetic_algorithm(map1, champ_list1, 20,10,10, 'cycle', 'inversion')
#time=map1.objective_fun(best_sol)
print(list_of_sol)
print(best_sol)
#print(time, best_sol.champ)




#Stworzenie algoroytmu ewlucyjnego:
#Badanie populacji
#Metoda selekcji
#sąsiedztwo
#przebieg algorytmu
#nakład obliczeniowy
#21/22 stycznia?? kolokwium


#Działanie algorytmu -> Losowanie paru rozwiazań ()