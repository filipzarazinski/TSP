from tkinter import*
import numpy as np
import random
import time
import math
import tkinter
import numpy
from tkinter import filedialog




class TabuSearchTSP:
    def __init__(self, distance_matrix, max_distance):
        
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.max_distance = max_distance
        self.best_solution = None
        self.best_cost = float('inf')
        self.iterations = 0

    def initial_solution(self):
        value = selected_option1.get()
   
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
        elif value == "symulowane":
            solution2 = list(range(self.num_cities))
            random.shuffle(solution2)
            solution = self.simulated_annealing(solution2,10000,0.99)
            

        else:
            print("nie wybrano!!")    
        
        
        return solution

    def calculate_cost(self, solution):
        
        total_distance = 0
        number_of_cities = len(solution)
    
        for i in range(number_of_cities - 1):
            total_distance += distance_matrix[solution[i]][solution[i + 1]]
        
        # Dodaj odległość powrotną z ostatniego miasta do pierwszego
        total_distance += distance_matrix[solution[-1]][solution[0]]
        return total_distance




    def swap(self, solution):
        value = selected_option2.get()
        if value == "swap_dwa_miasta":
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
        elif value == "swap_2opt":
            n = self.num_cities
            a, b = sorted(random.sample(range(n), 2))
            if a + 1 == b:
                return solution  
            new_solution = solution[:a+1] + solution[b:a:-1] + solution[b+1:]
            return new_solution
        elif value == "insert":
            n = len(solution)

            city_to_move = random.randint(0, n-1)
            insert_position = random.randint(0, n-2)

            if insert_position >= city_to_move:
                insert_position += 1

            new_solution = solution[:city_to_move] + solution[city_to_move+1:]
            new_solution = new_solution[:insert_position] + [solution[city_to_move]] + new_solution[insert_position:]

            return new_solution
        elif value == "reverse":
            n = len(solution)
            
            start = random.randint(0, n-2)
            end = random.randint(start+1, n-1)

            
            new_solution = solution[:start] + solution[start:end+1][::-1] + solution[end+1:]
            return new_solution
        elif value == "or-opt":
            n = len(solution)
            
            segment_length = 3  
            start = random.randint(0, n - segment_length - 1)
            end = start + segment_length
    
            insert_position = random.randint(0, n - segment_length - 2)
            if insert_position >= start:
                insert_position += segment_length

            
            segment_to_move = solution[start:end]
            new_solution = solution[:start] + solution[end:]
            new_solution = new_solution[:insert_position] + segment_to_move + new_solution[insert_position:]
            return new_solution
        else:
            print("error")
            return 0

        

    def solve(self):
        
        current_solution = self.initial_solution()

        current_cost = self.calculate_cost(current_solution)
        
        i=0
        tabu_list = []

        
        if current_cost < self.max_distance:
            self.best_cost = current_cost
            self.best_solution = current_solution
            self.iterations = 0
        #for _ in range(self.max_distance):
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
                #print(f"Aktualnie: {self.best_cost}")
           
        

        return self.best_solution, self.best_cost, self.iterations
    
    
    
    def simulated_annealing(self,initial_solution, temperature, cooling_rate):
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
    total_cost = 0
    start_time = time.time()
    for _ in range(iterations):
        print(_)
        tsp_solver = TabuSearchTSP(distance_matrix, max_distance)
        solution, cost, iter = tsp_solver.solve()
        print('Rozwiązanie:', cost)
        total_cost = total_cost + cost
        total_iter = total_iter + iter
    average = total_iter / iterations
    end_time = time.time()
    elapsed_time = end_time - start_time
    mean_time = elapsed_time / iterations
    print("Czas testu TS =:",elapsed_time,"s")
    print(f"Średni czas wykonania 1 algorytmu: {mean_time} s")
    print(f"Średni koszt: {total_cost/iterations} s")
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




okno =Tk()
okno.geometry('480x480')
okno.resizable(False,False)
okno.wm_title("TSP - Tabu Search")

insert = Entry(okno,width=12)
insert2 = Entry(okno,width=12)
insert3 = Entry(okno,width=12)
button = tkinter.Button(okno, text='Tabu-search',command=lambda:Tabu_search_run(int(insert.get())))
button2 = tkinter.Button(okno, text='Tabu-search-test',command=lambda:Tabu_test(int(insert.get()),int(insert2.get())))
button3 = tkinter.Button(okno, text='Visual',)
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
selected_option1 = tkinter.StringVar(okno)
selected_option2 = tkinter.StringVar(okno)

opcje1 = ["losowo", "zachlanny","symulowane"]
option_menu1 = tkinter.OptionMenu(okno, selected_option1, *opcje1)
option_menu1.pack()
option_menu1.place(x=20,y=260)

opcje2 = ["swap_dwa_miasta", "swap_2opt", "insert","reverse","or-opt"]
option_menu2 = tkinter.OptionMenu(okno, selected_option2, *opcje2)
option_menu2.pack()
option_menu2.place(x=140,y=260)



okno.mainloop()
        
    