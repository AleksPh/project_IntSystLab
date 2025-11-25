import math
import random
import heapq
from collections import deque
from constants import (
    PACMAN_SPEED, GHOST_SPEED, GHOST_VISION_RANGE, 
    GHOST_MEMORY_TIME, PATROL_POINTS, MAZE_WIDTH, MAZE_HEIGHT,
    Difficulty
)


class Pacman:    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = PACMAN_SPEED
        self.auto_mode = False
        self.target = None
    
    def update(self, maze, ghosts):
        """Оновлення позицію пакмена"""
        if self.next_direction != (0, 0):
            test_x = self.x + self.next_direction[0] * self.speed
            test_y = self.y + self.next_direction[1] * self.speed
            
            if not maze.is_wall(test_x, test_y):
                self.direction = self.next_direction
        
        if self.direction != (0, 0):
            new_x = self.x + self.direction[0] * self.speed
            new_y = self.y + self.direction[1] * self.speed
            
            if not maze.is_wall(new_x, new_y):
                self.x = new_x
                self.y = new_y
    
    def auto_move(self, maze, ghosts):
        """Автоматичний рух пакмена"""
        if not self.auto_mode:
            return
        
        # Знаходження найближчого привида
        nearest_ghost_dist = float('inf')
        for ghost in ghosts:
            dist = math.sqrt((self.x - ghost.x)**2 + (self.y - ghost.y)**2)
            if dist < nearest_ghost_dist:
                nearest_ghost_dist = dist
        
        # привид близько -> run
        if nearest_ghost_dist < 4:
            best_dir = self.find_escape_direction(maze, ghosts)
        else:
            best_dir = self.find_dot_direction(maze)
        
        if best_dir:
            self.next_direction = best_dir
    
    def find_escape_direction(self, maze, ghosts):
        """напрямок втечі від привидів"""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        best_dir = None
        max_dist = -1
        
        for dx, dy in directions:
            test_x = self.x + dx * 0.5
            test_y = self.y + dy * 0.5
            
            if not maze.is_wall(test_x, test_y):
                #  мінімальнa відстань до привидів
                min_ghost_dist = float('inf')
                for ghost in ghosts:
                    dist = math.sqrt((test_x - ghost.x)**2 + (test_y - ghost.y)**2)
                    min_ghost_dist = min(min_ghost_dist, dist)
                
                if min_ghost_dist > max_dist:
                    max_dist = min_ghost_dist
                    best_dir = (dx, dy)
        
        return best_dir
    
    def find_dot_direction(self, maze):
        """Знаходить напрямок до найближчої точки"""
        if not maze.dots:
            return None
        
        # Знаходимо найближчу точку
        min_dist = float('inf')
        target = None
        for dot in maze.dots[:15]:
            dist = abs(self.x - dot[0]) + abs(self.y - dot[1])
            if dist < min_dist:
                min_dist = dist
                target = dot
        
        if not target:
            return None
        
        # Простий напрямок до цілі
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        best_dir = None
        min_dist = float('inf')
        
        for dx, dy in directions:
            test_x = self.x + dx * 0.5
            test_y = self.y + dy * 0.5
            
            if not maze.is_wall(test_x, test_y):
                dist = abs(test_x - target[0]) + abs(test_y - target[1])
                if dist < min_dist:
                    min_dist = dist
                    best_dir = (dx, dy)
        
        return best_dir


class Ghost:
    
    def __init__(self, x, y, color, personality):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.personality = personality  # 'aggressive', 'strategic', 'random', 'patrol'
        self.speed = GHOST_SPEED
        self.target = None
        self.path = []
        self.last_seen_pacman = None
        self.memory_time = 0
        self.vision_range = GHOST_VISION_RANGE
        self.scatter_target = (random.randint(2, MAZE_WIDTH-3), random.randint(2, MAZE_HEIGHT-3))
        self.patrol_points = PATROL_POINTS
        self.patrol_index = 0
    
    def can_see_pacman(self, pacman, maze):
        """Перевірка чи привид бачить пакмена (з урахуванням стін)"""
        dist = math.sqrt((self.x - pacman.x)**2 + (self.y - pacman.y)**2)
        
        if dist > self.vision_range:
            return False
        
        # Простий raycast
        steps = int(dist * 3)
        if steps == 0:
            return True
            
        for i in range(1, steps):
            t = i / steps
            check_x = self.x + (pacman.x - self.x) * t
            check_y = self.y + (pacman.y - self.y) * t
            if maze.is_wall(check_x, check_y):
                return False
        
        return True
    
    def update_memory(self, pacman, maze):
        """Оновлення пам'ять про останню позицію пакмена"""
        if self.can_see_pacman(pacman, maze):
            self.last_seen_pacman = (int(round(pacman.x)), int(round(pacman.y)))
            self.memory_time = GHOST_MEMORY_TIME
        elif self.memory_time > 0:
            self.memory_time -= 1
            if self.memory_time == 0:
                self.last_seen_pacman = None
    
    def get_target(self, pacman, maze, other_ghosts, difficulty):
        """Визначає ціль привида залежно від особистості та складності"""
        
        # Легкий рівень - проста поведінка
        if difficulty == Difficulty.EASY:
            if self.can_see_pacman(pacman, maze):
                return (int(round(pacman.x)), int(round(pacman.y)))
            else:
                return self.scatter_target
        
        # Середній рівень - з пам'яттю
        if difficulty == Difficulty.MEDIUM:
            if self.can_see_pacman(pacman, maze):
                return (int(round(pacman.x)), int(round(pacman.y)))
            elif self.last_seen_pacman and self.memory_time > 0:
                return self.last_seen_pacman
            else:
                return self.scatter_target
        
        # Важкий рівень - повна поведінка з особистостями
        if self.personality == 'aggressive':
            # Агресивний - переслідує безпосередньо
            if self.can_see_pacman(pacman, maze):
                return (int(round(pacman.x)), int(round(pacman.y)))
            elif self.last_seen_pacman and self.memory_time > 0:
                return self.last_seen_pacman
            else:
                return self.scatter_target
        
        elif self.personality == 'strategic':
            # Стратегічний - намагається перехопити
            if self.can_see_pacman(pacman, maze):
                # Прогнозує рух пакмена
                predict_x = int(round(pacman.x + pacman.direction[0] * 2))
                predict_y = int(round(pacman.y + pacman.direction[1] * 2))
                if not maze.is_wall(predict_x, predict_y):
                    return (predict_x, predict_y)
                return (int(round(pacman.x)), int(round(pacman.y)))
            elif self.last_seen_pacman and self.memory_time > 0:
                return self.last_seen_pacman
            else:
                return self.scatter_target
        
        elif self.personality == 'patrol':
            # Патрулює ключові точки
            if self.can_see_pacman(pacman, maze):
                return (int(round(pacman.x)), int(round(pacman.y)))
            else:
                target = self.patrol_points[self.patrol_index]
                dist = abs(self.x - target[0]) + abs(self.y - target[1])
                if dist < 1:
                    self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)
                return target
        
        else:  # random
            # Випадковий - змішана поведінка
            if self.can_see_pacman(pacman, maze) and random.random() > 0.4:
                return (int(round(pacman.x)), int(round(pacman.y)))
            else:
                return self.scatter_target
    
    def avoid_collision(self, target, other_ghosts):
        """Уникнення зіткнень з іншими привидами"""
        if not target:
            return target
        
        for ghost in other_ghosts:
            if ghost is self:
                continue
            
            if ghost.target == target:
                dist_to_target = abs(self.x - target[0]) + abs(self.y - target[1])
                ghost_dist_to_target = abs(ghost.x - target[0]) + abs(ghost.y - target[1])
                
                if ghost_dist_to_target < dist_to_target:
                    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    for dx, dy in offsets:
                        new_target = (target[0] + dx, target[1] + dy)
                        if 0 < new_target[0] < MAZE_WIDTH-1 and 0 < new_target[1] < MAZE_HEIGHT-1:
                            return new_target
        
        return target
    
    def find_path_bfs(self, target, maze):
        """Алгоритм BFS для пошуку шляху"""
        if not target:
            return []
        
        start = (int(round(self.x)), int(round(self.y)))
        if start == target:
            return []
        
        queue = deque([(start, [start])])
        visited = {start}
        
        max_iterations = 200
        iterations = 0
        
        while queue and iterations < max_iterations:
            iterations += 1
            (x, y), path = queue.popleft()
            
            if (x, y) == target:
                return path
            
            for nx, ny in maze.get_neighbors(x, y):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return []
    
    def find_path_astar(self, target, maze):
        """Алгоритм A* для пошуку шляху"""
        if not target:
            return []
        
        start = (int(round(self.x)), int(round(self.y)))
        if start == target:
            return []
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, target)}
        
        max_iterations = 200
        iterations = 0
        
        while open_set and iterations < max_iterations:
            iterations += 1
            _, current = heapq.heappop(open_set)
            
            if current == target:
                # Відновлення шлях
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            
            for neighbor in maze.get_neighbors(current[0], current[1]):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []
    
    def update(self, pacman, maze, other_ghosts, difficulty):
        """Оновлює позицію привида"""
        self.update_memory(pacman, maze)       
        target = self.get_target(pacman, maze, other_ghosts, difficulty)
        
        if difficulty == Difficulty.HARD:
            target = self.avoid_collision(target, other_ghosts)
        
        self.target = target
        
        # Пошук шляху (A* для важкого рівня, BFS для інших)
        if difficulty == Difficulty.HARD:
            self.path = self.find_path_astar(target, maze)
        else:
            self.path = self.find_path_bfs(target, maze)
        
        # Рух по шляху
        if len(self.path) > 1:
            next_pos = self.path[1]
            dx = next_pos[0] - self.x
            dy = next_pos[1] - self.y
            
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                dx = (dx / dist) * self.speed
                dy = (dy / dist) * self.speed
                
                self.x += dx
                self.y += dy