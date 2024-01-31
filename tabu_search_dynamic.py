from tkinter import*
import numpy as np
import random
import time
import math
import tkinter
import numpy
from tkinter import filedialog
import tabu_search_func



class TabuSearchTSP:
    def __init__(self, distance_matrix, max_distance):
        
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.max_distance = max_distance
        self.best_solution = None
        self.best_cost = float('inf')
        self.iterations = 0

    def initial_solution(self):
        
        index = listbox.curselection()
        value = listbox.get(index)

        if value == "losowo":
            solution = list(range(self.num_cities))
            random.shuffle(solution)
        elif value == "zachlanny":
            current_city = 0
            solution = [current_city]
            unvisited = set(range(1, self.num_cities))
            while unvisited:
                next_city = min(unvisited, key=lambda city: self.distance_matrix[current_city][city])
                unvisited.remove(next_city)
                solution.append(next_city)
                current_city = next_city
        else:
            print("nie wybrano!!")    
        
        
        return solution

    def calculate_cost(self, solution):
        
        cost = sum(self.distance_matrix[solution[i]][solution[i + 1]] for i in range(self.num_cities - 1))
        cost += self.distance_matrix[solution[-1]][solution[0]]  
        return cost

    def swap_1(self, solution):
        
        a, b = random.sample(range(self.num_cities), 2)
        solution[a], solution[b] = solution[b], solution[a]
        return solution

    def swap(self, solution):
        num_swaps = int(insert3.get())
        best_solution = solution.copy()
        solutions = []

        for _ in range(num_swaps):
            new_solution = solution.copy()
            a, b = random.sample(range(self.num_cities), 2)
            new_solution[a], new_solution[b] = new_solution[b], new_solution[a]
            solutions.append(new_solution)
        
        best_solution = solutions[0]
        
        for _ in range(len(solutions)):
            if self.calculate_cost(best_solution) > self.calculate_cost(solutions[_]):
                best_solution = solutions[_]

        return best_solution

    def solve(self):
        
        current_solution = self.initial_solution()
       
        
        current_cost = self.calculate_cost(current_solution)
        i=0
        
        max_tabu_size = 200  # Maksymalna długość listy tabu
        min_tabu_size = 1  # Minimalna długość listy tabu
        tabu_list = []
        tabu_size = min_tabu_size  # Początkowa długość listy tabu
        no_improve_count = 0  # Licznik iteracji bez poprawy

        
        if current_cost < self.max_distance:
            self.best_cost = current_cost
            self.best_solution = current_solution
            self.iterations = 0
        while current_cost > self.max_distance:
        
            best_neighbor = None
            best_neighbor_cost = float('inf')
            self.iterations = self.iterations + 1
            
            
            for _ in range(self.num_cities):
                neighbor = self.swap(current_solution.copy())
                neighbor_cost = self.calculate_cost(neighbor)
                if neighbor_cost < best_neighbor_cost and neighbor not in tabu_list:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost

            
            if best_neighbor:
                current_solution = best_neighbor
                current_cost = best_neighbor_cost
                tabu_list.append(best_neighbor)
                tabu_list = tabu_list[-self.num_cities:] 

            if current_cost < self.best_cost:
                self.best_solution = current_solution
                self.best_cost = current_cost
                no_improve_count = 0  # Resetujemy licznik, ponieważ znaleźliśmy poprawę
                if tabu_size > min_tabu_size:  # Skracamy listę tabu, jeśli jest dłuższa niż minimalna
                    tabu_size -= 1
            else:
                no_improve_count += 1
                if no_improve_count >= self.num_cities and tabu_size < max_tabu_size:
                    # Rozszerzamy listę tabu, jeśli przez określoną liczbę iteracji nie było poprawy
                    tabu_size += 1
                    no_improve_count = 0

            # Przycinanie listy tabu do aktualnego rozmiaru
            tabu_list = tabu_list[-tabu_size:]
                #print(f"Aktualnie: {self.best_cost}")
           
        

        return self.best_solution, self.best_cost, self.iterations
    
    
    
    def simulated_annealing(self,initial_solution, distance_matrix, temperature, cooling_rate):
        current_solution = initial_solution.copy()
        current_cost = self.calculate_cost(current_solution)
        best_solution = current_solution
        best_cost = current_cost
        
        while temperature > 1:
            
            city1, city2 = random.sample(range(len(current_solution)), 2)
            new_solution = current_solution[:]
            new_solution[city1], new_solution[city2] = new_solution[city2], new_solution[city1]
            
            
            new_cost = self.calculate_cost(new_solution)
            
            
            cost_difference = new_cost - current_cost
            
            
            if cost_difference < 0 or math.exp(-cost_difference / temperature) > random.random():
                current_solution = new_solution
                current_cost = new_cost
                
                
                if current_cost < best_cost:
                    best_solution = current_solution
                    best_cost = current_cost
                    
            
            temperature *= cooling_rate

        return best_solution
def add_file():
        global file_name
        global distance_matrix
        file_name = filedialog.askopenfilename(initialdir='I:\TSP - projekt', title="Select File",
                                            filetypes=(("Comma-separated values", "*.txt"), ("all files", "*")))
        
        with open(file_name, 'r') as file:
            file_contents = file.read()
        tmp1 = file_name.split("/")[-1]
        tmp2 = tmp1.split(".")
        if file_name!="":
            addAppinfo = tkinter.Label()
            addAppinfo = tkinter.Label(text="                                                                                                                        ")
            addAppinfo.place(x=120, y=25)
            addAppinfo = tkinter.Label(text=f"Plik {tmp2[0]}.{tmp2[1]} załadowany")
            addAppinfo.place(x=120,y=25)
        distance_matrix = []
        for line in file_contents.strip().split('\n'):
            row = [int(x) for x in line.split()]
            distance_matrix.append(row)
        
        
    
def Tabu_test(max_distance,iterations):
    
    total_iter = 0
    start_time = time.time()
    for _ in range(iterations):
        print(_)
        tsp_solver = TabuSearchTSP(distance_matrix, max_distance)
        solution, cost, iter = tsp_solver.solve()
        print('Rozwiązanie:', cost)
        total_iter = total_iter + iter
    average = total_iter / iterations
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Czas testu TS =:",elapsed_time,"s")
    print(f'Tabu test, średnia: {average}')
    

def Tabu_search_run(max_distance):
    tsp_solver = TabuSearchTSP(distance_matrix, max_distance)
    start_time = time.time()
    solution, cost, iterations = tsp_solver.solve()
    print('Rozwiązanie:', solution)
    print('Koszt:', cost)
    print('Liczba iteracji:',iterations)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Czas pojedynczego TS =:",elapsed_time, "s")

    

def test(event):
    index = listbox.curselection()
    value = listbox.get(index)
    print(f'Wybrano: {value}')



okno =Tk()
okno.geometry('480x480')
okno.resizable(False,False)
okno.wm_title("TSP - Tabu Search")

insert = Entry(okno,width=12)
insert2 = Entry(okno,width=12)
insert3 = Entry(okno,width=12)
button = tkinter.Button(okno, text='Tabu-search',command=lambda:Tabu_search_run(int(insert.get())))
button2 = tkinter.Button(okno, text='Tabu-search-test',command=lambda:Tabu_test(int(insert.get()),int(insert2.get())))
button3 = tkinter.Button(okno, text='Check')
openFile = tkinter.Button(okno, text='Load file',command=lambda:add_file())

#labele
window_size = tkinter.Label(text="max_distance")
window_size.pack()
window_size.place(x=20,y=200)
time_size = tkinter.Label(text="test_number")
time_size.pack()
time_size.place(x=140,y=200)
number_swap = tkinter.Label(text="number_swap")
number_swap.pack()
number_swap.place(x=260,y=200)
#inserty
insert.pack()
insert.place(x=20,y=220)
insert2.pack()
insert2.place(x=140,y=220)
insert3.pack()
insert3.place(x=260,y=220)
#przyciski
button.pack()
button.place(x=20,y=60)
button2.pack()
button2.place(x=20,y=140)
button3.pack()
button3.place(x=20,y=100)
openFile.pack()
openFile.place(x=20,y=20)
#lista
listbox = tkinter.Listbox(okno)
listbox.pack()
listbox.place(x=20,y=260)
opcje = ["losowo", "zachlanny"]
for opcja in opcje:
    listbox.insert(tkinter.END, opcja)

listbox.bind('<<ListboxSelect>>', test)
okno.mainloop()
        
    