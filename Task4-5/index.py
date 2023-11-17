import seaborn as sns
import math
import random
import sys

import matplotlib.patches
import matplotlib.path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class Tower:
    """Класс вышки"""
    all_towers = [] # Переменная класса для хранения всех вышек. 
    
    # Переменная класса хранит последний свободный порядковый 
    # номер для инициализации вышки. 
    last__free_number_of_tower = 0 
    
    @staticmethod 
    def get_towers_obj_by_numbers(tower_numbers):
        # Получает массив из номеров башен и возвращает их объекты. 
        result = []
        for number in tower_numbers:
            for tower in Tower.all_towers:
                if tower.get_tower_number() == int(number):
                    result.append(tower)
        return result
    
    def __init__(self, x: int, y: int, R:int) -> None:
        """Иницилазция вышки

        Args:
            x (int): Координата x вышки на поле
            y (int): Координата y вышки на поле
        """
        # Порядковый номер вышки. 
        self.__number = Tower.last__free_number_of_tower
        Tower.last__free_number_of_tower += 1
        
        # Координаты вышки. 
        self.__x = x
        self.__y = y
        self.__R = R
        
        # Добавление новой вышки в классовую переменную. 
        Tower.all_towers.append(self)
    
    def get_tower_number(self):
        return self.__number
    
    def get_coord(self):
        return self.__x, self.__y
    
    def get_radius(self):
        return self.__R

class GridField:
    def __init__(self, non_obstructed: bool = True) -> None:
        """current field in city grid
        """
        self.__non_obstructed = non_obstructed # Является ли поле заблокированным. 
        self.__tower = False # Установлена ли на поле вышка.
         
        # Ссылка на объект вышки (если вышка не будет установлена 
        # на данном поле, переменная будет хранить None). 
        self.__tower_obj = None 
        
        self.__tower_cover = False # Покрывается ли поле какой-либо вышкой. 
        self.__tower_covered_list = [] # Список вышек, которые покрывают данное поле. 
        
    def __add_cover_tower(self, tower: Tower):
        if tower not in self.__tower_covered_list:
            self.__tower_covered_list.append(tower)
        
    def get_tower_covered_list(self):
        return self.__tower_covered_list
    
    def __set_tower_obj(self, obj: Tower):
        self.__tower_obj = obj
        
    def get_tower_obj(self):
        return self.__tower_obj
        
    def get_non_obstructed(self) -> bool:
        return self.__non_obstructed
    
    def set_non_obstructed(self, non_obstructed: bool) -> None:
        self.__non_obstructed = non_obstructed
    
    def set_tower(self, has_tower: bool, tower: Tower) -> None:
        # При установки вышки на поле, ссылка на объект вышки сохраняется 
        # в переменную tower_obj. 
        self.__tower = has_tower
        self.__set_tower_obj(tower)
 
    def get_tower(self) -> bool:
        return self.__tower
    
    def set_tower_cover(self, cover: bool, tower: Tower) -> None:
        # При установлении флага покрытия какой-либо вышкой, 
        # в переменную добавляется объект вышки. 
        self.__tower_cover = cover
        self.__add_cover_tower(tower)
    
    def get_tower_cover(self) -> bool:
        return self.__tower_cover

class CityGrid:
    # Класс сохраняет данные о поле, инициализирует его и генерирует начальное
    # покрытие блокированными и неблокированными блоками. 
    @staticmethod
    def initial_grid(n, m) -> None:
        """Method for initialize grid with GridField object"""
        
        grid = []
        for i in range(n):
            new_line = []
            for j in range(m):
                field = GridField()
                new_line.append(field)
            grid.append(new_line)
        return grid
                
    @staticmethod
    def coverage_grid(grid, n, m, coverage_percent) -> None:
        """Method for covering a field with obstructed blocks"""
        
        count_of_obstructed_blocks = math.ceil(n * m * coverage_percent / 100)
        done = 0
        while(done != count_of_obstructed_blocks):
            # Получение рандомных координта. 
            i = random.randint(0, n - 1)
            j = random.randint(0, m - 1)
            
            # Установка вышки (только на неблокированные блоки). 
            if grid[i][j].get_non_obstructed:
                grid[i][j].set_non_obstructed(False)
                done += 1
                
    @staticmethod
    def get_grid_for_seaborn_visualization(grid):
        """Метод для перевода сетки в тепловую карту"""
        lst = []
        for i in range(len(grid)):
            lst_line = []
            for j in range(len(grid[i])):
                if grid[i][j].get_non_obstructed():
                    if grid[i][j].get_tower():
                        lst_line.append(0.8) # Если на поле башня.
                    elif grid[i][j].get_tower_cover():
                        lst_line.append(0.5) # Если поле покрывается излучением башни. 
                    else:
                        lst_line.append(1) # Если поле неблокированное. 
                else:
                    lst_line.append(0) # Если поле блокированое. 
            lst.append(lst_line)
        return lst
    
    def __init__(self, N: int, M: int, coverage_percent: int = 30) -> None:
        self.__grid = CityGrid.initial_grid(N, M) # Initialize grid.
        CityGrid.coverage_grid(self.__grid, N, M, coverage_percent) # Grid covering.
    
    def get_grid(self):
        return self.__grid
    


class FieldCoverage:
    def __init__(self, grid, N, M, R):
        """Инициализация класса

        Args:
            grid (_type_): ссылка на сетку
            N (_type_): размер сетки
            M (_type_): размер сетки
            R (_type_): радиус действия вышек
        """
        self.__grid = grid
        self.__N = N
        self.__M = M
        self.__R = R
    
    def __tower_installation(self, x: int, y: int):
        """Метод для установки вышки на поле

        Args:
            x (int): индекс по x
            y (int): индекс по y
            R (int, optional): величина покрытия, где 0 - покрытие только самого 
            поля, где установлена башня, 1 - по одной клетки вокруг всех башни и т.д. 

        Raises:
            Exception: заданные индексы показывают на блокированный участок, где
            башня не может быть установлена. 
        """
        flag = True # Переменная необходима для поочередного изменения координат. 
        # Функция отнимает попеременно 1 от координат, пока координаты не будут
        # находится внутри сетки. 
        while x >= self.__N or y >= self.__M:
            if flag:
                x -= 1
            else:
                y -=1
            flag = not flag
            
        # Если поле заблокированно, используется метод для поиска новых координат. 
        if not self.__grid[x][y].get_non_obstructed():
            x, y = self.__search_new_place_for_tower(x, y)

        tower = Tower(x, y, self.__R)
        self.__grid[x][y].set_tower(True, tower) # Установка башни. 
        self.__grid[x][y].set_tower_cover(True, tower) # Данное поле автоматически становится покрытым. 
        
        # Установка покрытия на поле от башни для других полей сетки. 
        R = self.__R + 1
        for i in range(0 - R + 1, R):
            for j in range(0 - R + 1, R):
                if x - i < 0 or y - j < 0:
                    # Тепловая карта не имеет отрицательных значений, 
                    # поэтому итерацию необходимо пропустить. 
                    continue
                try:
                    if self.__grid[x - i][y - j].get_non_obstructed():
                        self.__grid[x-i][y-j].set_tower_cover(True, tower)
                except:
                    # Таких индексов на карте нет. 
                    pass
    
    def __search_new_place_for_tower(self, x, y):
        # Используем радиус вышки, чтобы итоговая вышка
        # была в районе переданного окна для ее установки. 
        R = self.__R + 1
        # Метод проходит вокруг изначальных координат, 
        # по заданному радиусу.  
        for i in range(R - 1, 0 - R, -1):
            for j in range(R - 1, 0 - R, -1):
                if x - i < 0 or y - j < 0:
                    # Если координат отрицательные, они вне сетки. 
                    continue
                try:
                    if self.__grid[x - i][y - j].get_non_obstructed():
                        return x - i, y - j
                except: 
                    pass
    
    def covered_field(self):
        # Метод покрывает поле вышками, пока все поле не будет покрыто. 
        while True:
            # Получение бинарной копии сетки, для более легких расчетов 
            # при установке вышки. 
            binary_grid = self.__get_binary_grid()
            # Получение левого верхнего угла окна (размер окна соотносится с радусом вышки), 
            # в котором будет установлена вышка. 
            start_x, start_y = self.__search_nearest_uncover_area(binary_grid)
            # Из метода возвращаются отрицательные координаты, когда все поле уже покыто. 
            if start_x == -1 and start_y == -1:
                break
            self.__best_place_for_tower(binary_grid, start_x, start_y)   

    def __get_binary_grid(self):
        """Метод для получение бинарной копии поля. 

        Returns:
            List[List[int]]: матрица из 0 и 1. 
        """
        binary_grid = []
        for i in range(self.__N):
            lst = []
            for j in range(self.__M):
                if self.__grid[i][j].get_tower_cover() or not self.__grid[i][j].get_non_obstructed():
                    lst.append(0)
                else:
                    lst.append(1)
            binary_grid.append(lst)
        return binary_grid
            
    def __search_nearest_uncover_area(self, binary_grid):
        """Метод ищет ближайшее непокрытое поле. 

        Args:
            binary_grid (List[List[int]]): матрица покрытия поля. 

        Returns:
            (int, int): координаты левого верхнего угла окна. 
        """
        start_x, start_y = 0, 0
        for i in range(self.__N):
            for j in range(self.__M):
                if binary_grid[i][j] == 1:
                    start_x = i
                    start_y = j
                    return start_x, start_y 
        return -1, -1
                    
                
    def __best_place_for_tower(self, binary_grid, start_x: int, start_y: int):
        window_side_length = self.__R * 2 + 1 # Середина окна. 
        window_filling = [] # Матрица из 0 и 1, которая хранит определенное окно поля. 
        for i in range(start_x, start_x + window_side_length):
            lst = []
            for j in range(start_y, start_y + window_side_length):
                if i >= self.__N or j >= self.__M:
                    # Перебор координат вышел из границ поля. 
                    continue
                lst.append(binary_grid[i][j])
            window_filling.append(lst)
            
        # Итоговые размеры окна (размеры могут быть меньше, так как окно 
        # может быть обрезано границами поля). 
        rows = len(window_filling) 
        columns = len(window_filling[0])
        
        # Установка вышки в середине окна (при невозможности поставить вышку по данным координатам
        # метод tower_installation изменит координаты на нужные). 
        self.__tower_installation(start_x + math.floor(rows / 2), start_y + math.floor(columns / 2))
      
class Draw:
    def __init__(self, grid, n, m) -> None:
        self.__field = grid
        self.__n = n
        self.__m = m
    
    def print_rectangle(self, axes, i, j, color = "k"):
        # Метод для рисования квардратов на поле. 
        rect_coord = [i, j]
        rect_width = 1
        rect_height = 1
        rect_angle = 0

        rect = matplotlib.patches.Rectangle(rect_coord, 
                                            rect_width, 
                                            rect_height, 
                                            rect_angle, 
                                            color=color)
        axes.add_patch(rect)
    
    def print_obstructed_blocks(self, axes):
        # Метод ищет все заблокированные блоки и выводит их. 
        for i in range(self.__n):
            for j in range(self.__m):
                if not self.__field[i][j].get_non_obstructed():
                    self.print_rectangle(axes, i, j)

    def print_tower(self, axes, x, y, number):
        # Метод предназначен для отрисовки башни.
        self.print_rectangle(axes, x, y, "red")
        plt.text(x + 0.3, y + 0.1, number, horizontalalignment="center")
    
    def print_towers(self, axes):
        # Метод перебирает башни и отправляет их в метод для отрисовки. 
        for tower in Tower.all_towers:
            x, y = tower.get_coord()
            self.print_tower(axes, x, y, tower.get_tower_number())
            
    def print_covered_blocks(self, axes):
        # Метод выводит покрытые блоки: желтый цвет - блок покрыт одной вышкой,
        # оранжевый - блок покрыт несколькими вышками. 
        for i in range(self.__n):
            for j in range(self.__m):
                if self.__field[i][j].get_non_obstructed():
                    if len(self.__field[i][j].get_tower_covered_list()) == 1:
                        self.print_rectangle(axes, i, j, 'yellow') 
                    else:
                        self.print_rectangle(axes, i, j, 'orange') 

    def print_grid(self, towers_obj):
        # Главный метод для отрисовки всей графики. 
        plt.xlim(0, self.__n)
        plt.ylim(0, self.__m)
        plt.grid()

        # Получим текущие оси
        axes = plt.gca()
        axes.set_aspect("equal")

        self.print_obstructed_blocks(axes) # Блокированные блоки. 
        self.print_covered_blocks(axes) # Покрытые блоки. 
        self.print_towers(axes) # Вышки. 
        if towers_obj is not None:
            self.__print_path(axes, towers_obj) # Путь между двумя выбранными вершинами

        plt.show()
        
    def __print_path(self, axes, towers_obj):
        # Метод выводит связи между выбранными вершинами
        for i in range(len(towers_obj) - 1):
            x0, y0 = towers_obj[i].get_coord()
            x1, y1 = towers_obj[i+1].get_coord()

            line = Line2D([x0, x1], [y0, y1], linewidth=0.4, color="red")
            axes.add_line(line)
    

class Graph:
    def __init__(self, towers, grid):
        self.__all_towers = [tower.get_tower_number() for tower in towers]
        self.__towers_len = len(self.__all_towers)
        self.__nodes = self.__initial_nodes() # Вершины графа
        self.__graph = self.__initial_graph(grid) # Ребра графа. 
        print(self.__graph)
    
    def __initial_nodes(self):
        nodes = []
        for i in range(self.__towers_len):
            nodes.append(str(i))
        return nodes
    
    def __initial_graph(self, grid):
        # Инициализация графа. 
        graph = {}
        for i in range(self.__towers_len):
            graph[str(i)] = {}
        # Заполнение графа значениями. 
        graph = self.__set_graph(graph, grid)
        return graph

    def __set_graph(self, graph, grid):
        # Создание словаря, вида {'0': {'1': 1}, '1': {'0': 1}}, где 
        # указаны все ребра графа. 
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                towers = grid[i][j].get_tower_covered_list()
                for k in range(len(towers)):
                    for p in range(len(towers)):
                        if k != p:
                            graph[str(towers[k].get_tower_number())][str(towers[p].get_tower_number())] = 1
                          
        return graph
    
    def get_graph(self):
        return self.__graph
    
    def get_nodes(self):
        return self.__nodes
    
    def get_outgoing_edges(self, node):
        # Возвращает связанные узлы. 
        connections = []
        for out_node in self.__nodes:
            if self.__graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        # Возвращает длину между узлами (фиксированная, так как проверяется надежность
        # связи между башнями). 
        return 1


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    shortest_path = {} # Кратчайшие пути до вершин. 
    previous_nodes = {} # Кратчайший найденный путь между узлами. 
  
    max_value = sys.maxsize # Бесконечно большое значение для непосещенных узлов. 
    for node in unvisited_nodes:
        shortest_path[node] = max_value
      
    shortest_path[start_node] = 0 # Начальный узел хранит расстояние - 0. 
    
    # Алгоритм выполняется до тех пор, пока все узлы не посещены. 
    while unvisited_nodes:
        # Поиск ближайшего узла. 
        current_min_node = None
        for node in unvisited_nodes: 
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # Извлечение соседей текущего узла и изменение расстояния до них. 
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node
 
        # Обозначение узла как посещенного.
        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path

def print_result(previous_nodes, start_node, end_node):
    path = []
    node = end_node
    
    while node != start_node:
        path.append(node)
        try: 
            node = previous_nodes[node]
        except:
            print("Вышки не связаны!")
            return
 
    path.append(start_node)
    print(" -> ".join(reversed(path)))
    return path
   
# Размеры поля 
N = 12
M = 8

# Радиус действия вышек. 
R = 3
# Инициализация поля, его размеров и радиуса действия вышек.
city_grid = CityGrid(N, M, coverage_percent=50)  

# Инициализация поля в классе, предназначенного для его покрытия.
field_coverage = FieldCoverage(city_grid.get_grid(), N, M, R)  

# Покрытие поле вышками. 
field_coverage.covered_field()

# Получение поля - объектов типа GridField
grid = city_grid.get_grid()

# Инициализация графа. 
graph = Graph(Tower.all_towers, grid) 


print("Выбрите две вершины из следующих (для поиска кратчашего расстояния): ", end = '')
print(*graph.get_nodes())
print("Вершина 1: ...")
start_node = input()
print("Вершина 2: ...")
end_node = input()

# Использование альгоритмы дейкстры, как результат: получение списка объектов в нужном порядке. 
# Если связи между вышками нет, путь между вершинами выводится на рисунке не будет. 
previous_nodes, shortest_path = dijkstra_algorithm(graph, start_node)
towers_obj = print_result(previous_nodes, start_node, end_node)

# Инициализация объекта для отрисовки всего поля. 
draw = Draw(city_grid.get_grid(), N, M)

# Отрисовка поля. 
if towers_obj is not None:
    # Связи между вышками есть, отрисовывется и путь между ними. 
    draw.print_grid(Tower.get_towers_obj_by_numbers(towers_obj))
else:
    # Связи между вышками нет (либо выбрана одна и та же вышка), путь не отрисовывается. 
    draw.print_grid(None)
    
