#tworzymy macierz dla danego przykłądu i zbioru wierzchołków dostępnych na początku
m1=[[100,5,5,14,16,12],[5,100,7,16,25,16],[5,7,100,12,16,14],[14,16,12,100,7,5],[16,25,16,7,100,5],[12,16,14,5,5,100]]
nodes=[1,2,3,4,5,6]
d_start=[1,3,4,6]


#definujemy parametry takie jak poziom, czasy celów i postacie (modyfikator postaci dla prędkości chodzenia i prędkości przechodzenia przez wierzchołki (robienia celów))
poziom=1
mod_p_move=1#stworzenie listy od jeden do 18 takiej że wartości przyjmowane są rozłożone od 1 do 0.8
mod_p_camp=1#stworzenie listy od jeden do 18 takiej że wartości przyjmowane są rozłożone od 1 do 0.5


#symulacja->losowanie rozwiązania, obliczanie funkcji celu dla tego rozwiązania
#first_node_index radnom number z przedziału 1 do 4
first_node=d_start[first_node_index]
#nodes pop 
for i in nodes:#stworzenie lsowej permutacji



#zbyt częste wykonywanie tego ruchu -> kara
#algorytm ewolucyjny???