import math
import random

class GridField:
    def __init__(self, non_obstructed: bool = True) -> None:
        """current field in city grid
        """
        self.__non_obstructed = non_obstructed 
        self.__tower = False 
        
    def get_non_obstructed(self) -> bool:
        return self.__non_obstructed
    
    def set_non_obstructed(self, non_obstructed: bool) -> None:
        self.__non_obstructed = non_obstructed
    
    def set_tower(self, has_tower: bool) -> None:
        self.__tower = has_tower
 
    def get_tower(self) -> bool:
        return self.__tower

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
    
    def __init__(self, N: int, M: int, coverage_percent: int = 30) -> None:
        self.__grid = CityGrid.initial_grid(N, M) # Initialize grid.
        CityGrid.coverage_grid(self.__grid, N, M, coverage_percent) # Grid covering.
    
    def get_grid(self):
        return self.__grid


def print_grid(grid):
    # Print grid like 0 (obstructed blocks) and 1 (non-obstructed blocks). 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].get_non_obstructed():
                print("1", end = ' ')
            else:
                print("0", end = ' ')
        print()
       
city_grid = CityGrid(N=5, M=7, coverage_percent=40)
print_grid(city_grid.get_grid()) 


   