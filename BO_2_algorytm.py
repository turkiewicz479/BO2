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

sol_list=[]
for j in range(10):
    curr_sol_time=200
    best_sol=None
    for i in range(10):

        sol_loop=map1.random_solution(champ_list1)
        sol_time=map1.objective_fun(sol_loop,sol_loop.champ)
        print(f'Wartość funkcji celu: {sol_time}\n')
        if sol_time<curr_sol_time:
            curr_sol_time=sol_time
            best_sol=sol_loop
        sol_loop.champ.reset()
    if best_sol != None:
        print("Najlepsze rozwiązanie z 10 losowych:")
        new_sol=map1.objective_fun(best_sol,best_sol.champ)
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