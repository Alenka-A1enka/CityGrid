import seaborn as sns
import matplotlib.pyplot as plt
import math
import random

class Tower:
    """Класс вышки"""
    all_towers = [] # Переменная класса для хранения всех вышек. 
    # Переменная класса хранит последний свободный порядковый 
    # номер для инициализации вышки. 
    last__free_number_of_tower = 0 
    
    def __init__(self, x: int, y: int) -> None:
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
        
        # Добавление новой вышки в классовую переменную. 
        Tower.all_towers.append(self)
    
    def get_tower_number(self):
        return self.__number

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

        tower = Tower(x, y)
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
      


def print_grid(grid):
    # Print grid like 0 (obstructed blocks) and 1 (non-obstructed blocks). 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].get_non_obstructed():
                print("1", end = ' ')
            else:
                print("0", end = ' ')
        print()
        

N = 15
M = 17
 
city_grid = CityGrid(N, M, coverage_percent=50)
field_coverage = FieldCoverage(city_grid.get_grid(), N, M, R = 3)

# Преобразование данных в нужный формат для вывода. 
data= CityGrid.get_grid_for_seaborn_visualization(city_grid.get_grid())

# Покрытие поле вышками. 
field_coverage.covered_field()

# Вывод полученного поля. 
data= CityGrid.get_grid_for_seaborn_visualization(city_grid.get_grid())
sns.heatmap(data, fmt='.1g', vmin = 0, vmax = 1)
plt.show()

# Вывод на консоль информации о том, какими вышками покрыта каждая 
# ячейка (блокированные ячейки не покрываются). 
grid = city_grid.get_grid()
for i in range(len(grid)):
    for j in range(len(grid[0])):
        towers = grid[i][j].get_tower_covered_list()
        print(f"Ячейка {i} {j}: ")
        for t in towers:
            print(f"Башня {t.get_tower_number()}")
        print()

