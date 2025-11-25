import pygame
import math
from maze import Maze
from entities import Pacman, Ghost
from constants import (
    WIDTH, HEIGHT, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT,
    BLACK, WHITE, BLUE, CYAN, YELLOW, RED, GREEN,
    GHOST_CONFIGS, GHOST_START_POSITIONS,
    POINTS_PER_DOT, SCORE_THRESHOLD_MEDIUM, SCORE_THRESHOLD_HARD,
    Difficulty
)


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman - Інтелектуальні привиди")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.difficulty = Difficulty.EASY
        self.score = 0
        self.level = 1
        self.debug_mode = False
        self.running = True
        self.game_over = False
        
        self.init_game()
    
    def init_game(self):
        self.maze = Maze()
        
        self.pacman = Pacman(2.5, 2.5)
        
        self.ghosts = []
        
        num_ghosts = 2 if self.difficulty == Difficulty.EASY else \
                    3 if self.difficulty == Difficulty.MEDIUM else 4
        
        for i in range(num_ghosts):
            color, personality = GHOST_CONFIGS[i]
            pos = GHOST_START_POSITIONS[i]
            self.ghosts.append(Ghost(pos[0], pos[1], color, personality))
    
    def check_collision(self):
        """Зіткнення пакмена з привидами"""
        for ghost in self.ghosts:
            dist = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
            if dist < 0.6:
                return True
        return False
    
    def collect_dots(self):
        """Збір точок"""
        pacman_cell = (int(round(self.pacman.x)), int(round(self.pacman.y)))
        if pacman_cell in self.maze.dots:
            self.maze.dots.remove(pacman_cell)
            self.score += POINTS_PER_DOT
            
            # Автоматичне підвищення складності
            if self.score >= SCORE_THRESHOLD_MEDIUM and self.difficulty == Difficulty.EASY:
                self.difficulty = Difficulty.MEDIUM
                self.init_game()
                print("Складність підвищено до СЕРЕДНЬОГО")
            elif self.score >= SCORE_THRESHOLD_HARD and self.difficulty == Difficulty.MEDIUM:
                self.difficulty = Difficulty.HARD
                self.init_game()
                print("Складність підвищено до ВАЖКОГО")
    
    def next_level(self):
        self.level += 1
        self.init_game()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Керування пакменом
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = (1, 0)
                
                # Перемикання складності
                elif event.key == pygame.K_1:
                    self.difficulty = Difficulty.EASY
                    self.init_game()
                    print("Складність: ЛЕГКА")
                elif event.key == pygame.K_2:
                    self.difficulty = Difficulty.MEDIUM
                    self.init_game()
                    print("Складність: СЕРЕДНЯ")
                elif event.key == pygame.K_3:
                    self.difficulty = Difficulty.HARD
                    self.init_game()
                    print("Складність: ВАЖКА")
                
                # Інші функції
                elif event.key == pygame.K_r:
                    self.game_over = False
                    self.score = 0
                    self.level = 1
                    self.difficulty = Difficulty.EASY
                    self.init_game()
                elif event.key == pygame.K_SPACE:
                    self.pacman.auto_mode = not self.pacman.auto_mode
                    print(f"Авто-режим: {'ВКЛ' if self.pacman.auto_mode else 'ВИКЛ'}")
                elif event.key == pygame.K_d:
                    self.debug_mode = not self.debug_mode
        
        # Перевірка утримання клавіші D
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.debug_mode = True
        else:
            self.debug_mode = False
    
    def update(self):
        """Оновлює стан гри"""
        if self.game_over:
            return
        
        if self.pacman.auto_mode:
            self.pacman.auto_move(self.maze, self.ghosts)
        self.pacman.update(self.maze, self.ghosts)
        
        for ghost in self.ghosts:
            ghost.update(self.pacman, self.maze, self.ghosts, self.difficulty)
        
        if self.check_collision():
            self.game_over = True
            print("GAME OVER!")
        
        self.collect_dots()
        
        if not self.maze.dots and not self.game_over:
            print(f"Рівень {self.level} пройдено!")
            self.next_level()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        #  лабіринт
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 0:
                    pygame.draw.rect(self.screen, BLUE, 
                                   (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, CYAN, 
                                   (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        #  точки
        for dot in self.maze.dots:
            pygame.draw.circle(self.screen, WHITE, 
                             (int(dot[0] * CELL_SIZE + CELL_SIZE/2), 
                              int(dot[1] * CELL_SIZE + CELL_SIZE/2)), 4)
        
        # Режим налагодження
        if self.debug_mode:
            for ghost in self.ghosts:
                # Зона видимості
                pygame.draw.circle(self.screen, ghost.color,
                                 (int(ghost.x * CELL_SIZE + CELL_SIZE/2),
                                  int(ghost.y * CELL_SIZE + CELL_SIZE/2)),
                                 int(ghost.vision_range * CELL_SIZE), 1)
                
                # Шлях
                if ghost.path:
                    for i in range(len(ghost.path) - 1):
                        start = (ghost.path[i][0] * CELL_SIZE + CELL_SIZE//2,
                               ghost.path[i][1] * CELL_SIZE + CELL_SIZE//2)
                        end = (ghost.path[i+1][0] * CELL_SIZE + CELL_SIZE//2,
                             ghost.path[i+1][1] * CELL_SIZE + CELL_SIZE//2)
                        pygame.draw.line(self.screen, ghost.color, start, end, 2)
                
                # Ціль
                if ghost.target:
                    pygame.draw.rect(self.screen, ghost.color,
                                   (ghost.target[0] * CELL_SIZE + 5,
                                    ghost.target[1] * CELL_SIZE + 5,
                                    CELL_SIZE - 10, CELL_SIZE - 10), 2)
        
        # привиди
        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, ghost.color,
                             (int(ghost.x * CELL_SIZE + CELL_SIZE/2),
                              int(ghost.y * CELL_SIZE + CELL_SIZE/2)),
                             CELL_SIZE // 2 - 4)
            # Очі
            eye_offset = CELL_SIZE // 6
            pygame.draw.circle(self.screen, WHITE,
                             (int(ghost.x * CELL_SIZE + CELL_SIZE/2 - eye_offset),
                              int(ghost.y * CELL_SIZE + CELL_SIZE/2 - eye_offset)), 4)
            pygame.draw.circle(self.screen, WHITE,
                             (int(ghost.x * CELL_SIZE + CELL_SIZE/2 + eye_offset),
                              int(ghost.y * CELL_SIZE + CELL_SIZE/2 - eye_offset)), 4)
            pygame.draw.circle(self.screen, BLACK,
                             (int(ghost.x * CELL_SIZE + CELL_SIZE/2 - eye_offset),
                              int(ghost.y * CELL_SIZE + CELL_SIZE/2 - eye_offset)), 2)
            pygame.draw.circle(self.screen, BLACK,
                             (int(ghost.x * CELL_SIZE + CELL_SIZE/2 + eye_offset),
                              int(ghost.y * CELL_SIZE + CELL_SIZE/2 - eye_offset)), 2)
        
        #  пакмена
        center = (int(self.pacman.x * CELL_SIZE + CELL_SIZE/2),
                 int(self.pacman.y * CELL_SIZE + CELL_SIZE/2))
        pygame.draw.circle(self.screen, YELLOW, center, CELL_SIZE // 2 - 4)
        
        if self.pacman.direction != (0, 0):
            mouth_angle = 30
            start_angle = math.atan2(-self.pacman.direction[1], self.pacman.direction[0])
            start_angle = math.degrees(start_angle)
            pygame.draw.polygon(self.screen, BLACK, [
                center,
                (center[0] + math.cos(math.radians(start_angle + mouth_angle)) * (CELL_SIZE//2),
                 center[1] - math.sin(math.radians(start_angle + mouth_angle)) * (CELL_SIZE//2)),
                (center[0] + math.cos(math.radians(start_angle - mouth_angle)) * (CELL_SIZE//2),
                 center[1] - math.sin(math.radians(start_angle - mouth_angle)) * (CELL_SIZE//2))
            ])
        
        # Інтерфейс
        y_offset = MAZE_HEIGHT * CELL_SIZE + 10
        
        score_text = self.small_font.render(f"Рахунок: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, y_offset))
        
        level_text = self.small_font.render(f"Рівень: {self.level}", True, WHITE)
        self.screen.blit(level_text, (150, y_offset))
        
        diff_names = {Difficulty.EASY: "ЛЕГКА", Difficulty.MEDIUM: "СЕРЕДНЯ", Difficulty.HARD: "ВАЖКА"}
        diff_text = self.small_font.render(f"Складність: {diff_names[self.difficulty]}", True, WHITE)
        self.screen.blit(diff_text, (280, y_offset))
        
        mode_text = self.small_font.render(f"Режим: {'АВТО' if self.pacman.auto_mode else 'РУЧНИЙ'}", 
                                          True, GREEN if self.pacman.auto_mode else WHITE)
        self.screen.blit(mode_text, (10, y_offset + 30))
        
        help_text = self.small_font.render("Стрілки-рух | 1/2/3-складність | SPACE-авто | D-debug | R-рестарт", 
                                          True, WHITE)
        self.screen.blit(help_text, (10, y_offset + 55))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Натисніть R", True, RED)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            pygame.draw.rect(self.screen, BLACK, (text_rect.x - 10, text_rect.y - 10, 
                                                  text_rect.width + 20, text_rect.height + 20))
            pygame.draw.rect(self.screen, RED, (text_rect.x - 10, text_rect.y - 10, 
                                               text_rect.width + 20, text_rect.height + 20), 3)
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Головний ігровий цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()