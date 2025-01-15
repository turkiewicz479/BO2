from Klasy_i_funkcje import *
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GeneticAlgorithmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja algorytmu genetycznego")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)





        self.settings_frame = ttk.Frame(self.notebook)
        self.results_frame = ttk.Frame(self.notebook)
        self.settings_frame.rowconfigure(10, weight=1)
        self.settings_frame.columnconfigure(0, weight=1) 
        self.settings_frame.columnconfigure(1, weight=1)  
        self.notebook.add(self.settings_frame, text="Ustawienia i wyniki")
        self.notebook.add(self.results_frame, text="Wykres wyników")

        self.map_size_label = tk.Label(self.settings_frame, text="Wielkość mapy:")
        self.map_size_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.map_size_entry = tk.Entry(self.settings_frame)
        self.map_size_entry.grid(row=0, column=1, padx=5, pady=5)

        self.d_start_size_label = tk.Label(self.settings_frame, text="Ilość wierzchołków startowych:")
        self.d_start_size_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.d_start_size_entry = tk.Entry(self.settings_frame)
        self.d_start_size_entry.grid(row=1, column=1, padx=5, pady=5)

        self.d_end_size_label = tk.Label(self.settings_frame, text="Ilość wierzchołków końcowych:")
        self.d_end_size_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.d_end_size_entry = tk.Entry(self.settings_frame)
        self.d_end_size_entry.grid(row=2, column=1, padx=5, pady=5)

        self.crossover_label = tk.Label(self.settings_frame, text="Typ krzyżowania:")
        self.crossover_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.crossover_var = tk.StringVar(value="pmx")
        self.crossover_menu = ttk.Combobox(self.settings_frame, textvariable=self.crossover_var, values=["pmx", "cycle", "order"], state="readonly")
        self.crossover_menu.grid(row=3, column=1, padx=5, pady=5)

        self.mutation_label = tk.Label(self.settings_frame, text="Typ mutacji:")
        self.mutation_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.mutation_var = tk.StringVar(value="swap")
        self.mutation_menu = ttk.Combobox(self.settings_frame, textvariable=self.mutation_var, values=["swap", "inversion", "champ"], state="readonly")
        self.mutation_menu.grid(row=4, column=1, padx=5, pady=5)

        self.population_size_label = tk.Label(self.settings_frame, text="Wielkość populacji:")
        self.population_size_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.population_size_entry = tk.Entry(self.settings_frame)
        self.population_size_entry.grid(row=5, column=1, padx=5, pady=5)

        self.num_generations_label = tk.Label(self.settings_frame, text="Liczba generacji:")
        self.num_generations_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.num_generations_entry = tk.Entry(self.settings_frame)
        self.num_generations_entry.grid(row=6, column=1, padx=5, pady=5)

        self.mutation_rate_label = tk.Label(self.settings_frame, text="Procent mutacji:")
        self.mutation_rate_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.mutation_rate_entry = tk.Entry(self.settings_frame)
        self.mutation_rate_entry.grid(row=7, column=1, padx=5, pady=5)

        self.generate_map_button = tk.Button(self.settings_frame, text="Generuj mapę", command=self.generate_map)
        self.generate_map_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.run_button = tk.Button(self.settings_frame, text="Uruchom algorytm", command=self.run_algorithm)
        self.run_button.grid(row=9, column=0, columnspan=2, pady=10) 

        self.results_text = tk.Text(self.settings_frame, height=10, width=50)
        self.results_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")



        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title("Jakość rozwiązań w kolejnych generacjach")
        self.ax.set_xlabel("Generacja")
        self.ax.set_ylabel("Czas rozwiązania")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.results_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.generations = []
        self.scores = []


        self.map2 = None

    def generate_map(self):
        try:
            map_size = int(self.map_size_entry.get())
            d_start_size = int(self.d_start_size_entry.get())
            d_end_size = int(self.d_end_size_entry.get())

            d_start = generate_unique_numbers(d_start_size, 0, map_size-1)
            d_end = generate_unique_numbers(d_end_size, 0, map_size-1)
            m2, nodes_time = generate_map(map_size)
            self.map2 = Mapa(m2, d_start, d_end, nodes_time)

            self.results_text.insert(tk.END, "Mapa została wygenerowana poprawnie.\n")
        except Exception as e:
            self.results_text.insert(tk.END, f"Błąd podczas generowania mapy: {e}\n")

    def run_algorithm(self):
        try:
            if not self.map2:
                raise ValueError("Najpierw wygeneruj mapę!")

            population_size = int(self.population_size_entry.get())
            num_generations = int(self.num_generations_entry.get())
            mutation_rate = int(self.mutation_rate_entry.get())
            crossover_type = self.crossover_var.get()
            mutation_type = self.mutation_var.get()

            list_of_sol, best_sol = genetic_algorithm(self.map2, champ_list1, population_size, mutation_rate,num_generations, crossover_type, mutation_type)

            self.generations = list(range(1, len(list_of_sol) + 1))
            self.scores = [sol.time for sol in list_of_sol]
            self.ax.clear()
            self.ax.plot(self.generations, self.scores, marker="o")
            self.ax.set_title("Jakość rozwiązań w kolejnych generacjach")
            self.ax.set_xlabel("Generacja")
            self.ax.set_ylabel("Czas rozwiązania")
            self.canvas.draw()

            self.results_text.insert(tk.END, f"Najlepsze rozwiązanie: \n{best_sol[0]}\n")
        except Exception as e:
            self.results_text.insert(tk.END, f"Błąd podczas uruchamiania algorytmu: {e}\n")


def main():
    app = GeneticAlgorithmApp()
    app.mainloop()


if __name__ == "__main__":
    main()
