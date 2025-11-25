from enum import Enum

# Розміри
CELL_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
WIDTH = MAZE_WIDTH * CELL_SIZE
HEIGHT = MAZE_HEIGHT * CELL_SIZE + 100

# Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# Налаштування гри
PACMAN_SPEED = 0.12
GHOST_SPEED = 0.08
GHOST_VISION_RANGE = 6
GHOST_MEMORY_TIME = 80

# Пороги складності
SCORE_THRESHOLD_MEDIUM = 300
SCORE_THRESHOLD_HARD = 600

# Очки
POINTS_PER_DOT = 10

class Difficulty(Enum):
    """Рівні складності гри"""
    EASY = 1
    MEDIUM = 2
    HARD = 3

# Конфігурація привидів
GHOST_CONFIGS = [
    (RED, 'aggressive'),
    (PINK, 'strategic'),
    (CYAN, 'patrol'),
    (ORANGE, 'random')
]

# Стартові позиції привидів
GHOST_START_POSITIONS = [
    (MAZE_WIDTH - 3.5, MAZE_HEIGHT - 3.5),
    (2.5, MAZE_HEIGHT - 3.5),
    (MAZE_WIDTH - 3.5, 2.5),
    (MAZE_WIDTH // 2, MAZE_HEIGHT // 2)
]

# Патрульні точки для привидів
PATROL_POINTS = [
    (3, 3), 
    (MAZE_WIDTH - 4, 3), 
    (MAZE_WIDTH - 4, MAZE_HEIGHT - 4), 
    (3, MAZE_HEIGHT - 4)
]