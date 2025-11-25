import random
from constants import MAZE_WIDTH, MAZE_HEIGHT


class Maze:    
    def __init__(self):
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.grid = []
        self.dots = []
        self.generate()
    
    def generate(self):
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        #  зовнішні стіни
        for i in range(self.width):
            self.grid[0][i] = 0
            self.grid[self.height-1][i] = 0
        for i in range(self.height):
            self.grid[i][0] = 0
            self.grid[i][self.width-1] = 0
        
        # Горизонтальні стіни
        for i in range(2, self.width-2, 4):
            for j in range(4, 8):
                if self.grid[j][i] == 1:
                    self.grid[j][i] = 0
        
        # Вертикальні стіни
        for i in range(4, 8):
            for j in range(2, self.height-2, 4):
                if self.grid[j][i] == 1:
                    self.grid[j][i] = 0
        
        # Центральний блок
        center_x, center_y = self.width // 2, self.height // 2
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 < center_x + dx < self.width and 0 < center_y + dy < self.height:
                    self.grid[center_y + dy][center_x + dx] = 0
        
        # точки для збору
        self.dots = []
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                if self.grid[i][j] == 1:
                    self.dots.append((j, i))
    
    def is_wall(self, x, y):
        grid_x = int(round(x))
        grid_y = int(round(y))
        
        if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            return True
        return self.grid[grid_y][grid_x] == 0
    
    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not self.is_wall(nx, ny):
                neighbors.append((nx, ny))
        return neighbors