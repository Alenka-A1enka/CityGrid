import seaborn as sns
import matplotlib.pyplot as plt
import math
import random

class GridField:
    def __init__(self, non_obstructed: bool = True) -> None:
        """current field in city grid
        """
        self.__non_obstructed = non_obstructed # Является ли поле заблокированным. 
        self.__tower = False # Установлена ли на поле башня. 
        self.__tower_cover = False # Покрывается ли поле какой-либо башней. 
        
    def get_non_obstructed(self) -> bool:
        return self.__non_obstructed
    
    def set_non_obstructed(self, non_obstructed: bool) -> None:
        self.__non_obstructed = non_obstructed
    
    def set_tower(self, has_tower: bool) -> None:
        self.__tower = has_tower
 
    def get_tower(self) -> bool:
        return self.__tower
    
    def set_tower_cover(self, cover: bool) -> None:
        self.__tower_cover = cover
    
    def get_tower_cover(self) -> bool:
        return self.__tower_cover

class CityGrid:
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
            i = random.randint(0, n - 1)
            j = random.randint(0, m - 1)
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
    
    def tower_installation(self, x: int, y: int, R: int = 0):
        """Метод для установки вышки на поле

        Args:
            x (int): индекс по x
            y (int): индекс по y
            R (int, optional): величина покрытия, где 0 - покрытие только самого 
            поля, где установлена башня, 1 - по одной клетки вокруг всех башни и т.д. 

        Raises:
            Exception: заданные индексы показывают на блокированный участов, где
            башня не может быть установлена. 
        """
        if not self.__grid[x][y].get_non_obstructed():
            # Если поле блокированное на нем нельзя установить башню. 
            raise Exception("this field is obstructed")
        self.__grid[x][y].set_tower(True) # Установка башни. 
        self.__grid[x][y].set_tower_cover(True) # Установка покрытия. 
        
        # Установка покрытия на поле от башни для других полей сетки. 
        R += 1
        for i in range(0 - R + 1, R):
            for j in range(0 - R + 1, R):
                if x - i < 0 or y - j < 0:
                    # Тепловая карта не имеет отрицательных значений, 
                    # поэтому итерацию необходимо пропустить. 
                    continue
                try:
                    self.__grid[x-i][y-j].set_tower_cover(True)
                except:
                    # Таких индексов на карте нет. 
                    pass


def print_grid(grid):
    # Print grid like 0 (obstructed blocks) and 1 (non-obstructed blocks). 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].get_non_obstructed():
                print("1", end = ' ')
            else:
                print("0", end = ' ')
        print()
        
       
city_grid = CityGrid(N=5, M=7, coverage_percent=35)

city_grid.tower_installation(x=1, y=2, R=1)

# Преобразование данных в нужный формат для вывода. 
data= CityGrid.get_grid_for_seaborn_visualization(city_grid.get_grid())
print(data)

# Вывод данных на тепловой карте. 
sns.heatmap(data, annot = True, fmt='.1g')
plt.show()
