import pygame
import random
import sys
from enum import Enum

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BASE_GRID_SIZE = 20  # Базовый размер клетки

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Operation(Enum):
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    MODULO = "%"

class Difficulty(Enum):
    LEVEL_1 = "Однозначные (1-9)"
    LEVEL_2 = "Двузначные (10-99)"
    LEVEL_3 = "Трёхзначные (100-999)"
    LEVEL_4 = "Четырёхзначные (1000-9999)"
    LEVEL_5 = "Смешанные (1-9999)"

class ColorMode(Enum):
    DIFFERENT_COLORS = "Разные цвета (синий/красный)"
    SAME_COLOR = "Одинаковый цвет"

class MathSnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Математическая Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Состояние игры
        self.game_state = "menu"  # menu, game, game_over
        self.operation = Operation.ADDITION
        self.difficulty = Difficulty.LEVEL_1
        self.color_mode = ColorMode.DIFFERENT_COLORS
        self.score = 0
        
        # Динамические размеры
        self.grid_size = BASE_GRID_SIZE
        self.grid_width = WINDOW_WIDTH // self.grid_size
        self.grid_height = WINDOW_HEIGHT // self.grid_size
        
        # Змейка
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        
        # Математическое выражение и числа на поле
        self.current_expression = ""
        self.correct_answer = 0
        self.numbers_on_field = []
        
        self.update_grid_size()
        self.generate_new_expression()
        self.generate_numbers()
    
    def update_grid_size(self):
        """Обновляет размер сетки в зависимости от сложности"""
        if self.difficulty == Difficulty.LEVEL_1:
            self.grid_size = 30
            self.number_font = pygame.font.Font(None, 20)
        elif self.difficulty == Difficulty.LEVEL_2:
            self.grid_size = 35
            self.number_font = pygame.font.Font(None, 18)
        elif self.difficulty == Difficulty.LEVEL_3:
            self.grid_size = 45
            self.number_font = pygame.font.Font(None, 16)
        elif self.difficulty == Difficulty.LEVEL_4:
            self.grid_size = 55
            self.number_font = pygame.font.Font(None, 14)
        else:  # LEVEL_5
            self.grid_size = 50
            self.number_font = pygame.font.Font(None, 15)
        
        self.grid_width = WINDOW_WIDTH // self.grid_size
        self.grid_height = WINDOW_HEIGHT // self.grid_size

    def generate_new_expression(self):
        """Генерирует новое математическое выражение"""
        if self.difficulty == Difficulty.LEVEL_1:
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
        elif self.difficulty == Difficulty.LEVEL_2:
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
        elif self.difficulty == Difficulty.LEVEL_3:
            num1 = random.randint(100, 999)
            num2 = random.randint(100, 999)
        elif self.difficulty == Difficulty.LEVEL_4:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(1000, 9999)
        else:  # LEVEL_5 - смешанные
            num1 = random.randint(1, 9999)
            num2 = random.randint(1, 9999)
        
        # Для деления и модуло обеспечиваем целочисленный результат
        if self.operation == Operation.DIVISION:
            # Убеждаемся, что результат деления целый
            num1 = num2 * random.randint(1, 10)
            self.correct_answer = num1 // num2
        elif self.operation == Operation.MODULO:
            # Убеждаемся, что num2 больше 1
            if num2 == 1:
                num2 = 2
            self.correct_answer = num1 % num2
        elif self.operation == Operation.ADDITION:
            self.correct_answer = num1 + num2
        elif self.operation == Operation.SUBTRACTION:
            # Убеждаемся, что результат положительный
            if num1 < num2:
                num1, num2 = num2, num1
            self.correct_answer = num1 - num2
        elif self.operation == Operation.MULTIPLICATION:
            self.correct_answer = num1 * num2
        
        self.current_expression = f"{num1} {self.operation.value} {num2} = ?"
    
    def generate_numbers(self):
        """Генерирует числа на игровом поле"""
        self.numbers_on_field = []
        
        # Добавляем правильный ответ
        correct_pos = (random.randint(1, self.grid_width - 2), 
                      random.randint(3, self.grid_height - 2))
        self.numbers_on_field.append((correct_pos, self.correct_answer, True))
        
        # Добавляем неправильные ответы
        used_positions = {correct_pos}
        for _ in range(8):  # 8 неправильных ответов
            while True:
                pos = (random.randint(1, self.grid_width - 2), 
                      random.randint(3, self.grid_height - 2))
                if pos not in used_positions and pos not in self.snake:
                    used_positions.add(pos)
                    # Генерируем неправильный ответ
                    wrong_answer = self.generate_wrong_answer()
                    self.numbers_on_field.append((pos, wrong_answer, False))
                    break
    
    def generate_wrong_answer(self):
        """Генерирует неправильный ответ, близкий к правильному"""
        variation = random.randint(-10, 10)
        if variation == 0:
            variation = random.choice([-1, 1])
        wrong = self.correct_answer + variation
        return max(0, wrong)  # Не допускаем отрицательных чисел
    
    def handle_menu_events(self, event):
        """Обработка событий в меню"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.operation = Operation.ADDITION
            elif event.key == pygame.K_2:
                self.operation = Operation.SUBTRACTION
            elif event.key == pygame.K_3:
                self.operation = Operation.MULTIPLICATION
            elif event.key == pygame.K_4:
                self.operation = Operation.DIVISION
            elif event.key == pygame.K_5:
                self.operation = Operation.MODULO
            elif event.key == pygame.K_q:
                self.difficulty = Difficulty.LEVEL_1
                self.update_grid_size()
            elif event.key == pygame.K_w:
                self.difficulty = Difficulty.LEVEL_2
                self.update_grid_size()
            elif event.key == pygame.K_e:
                self.difficulty = Difficulty.LEVEL_3
                self.update_grid_size()
            elif event.key == pygame.K_r:
                self.difficulty = Difficulty.LEVEL_4
                self.update_grid_size()
            elif event.key == pygame.K_t:
                self.difficulty = Difficulty.LEVEL_5
                self.update_grid_size()
            elif event.key == pygame.K_c:
                # Переключение цветового режима
                if self.color_mode == ColorMode.DIFFERENT_COLORS:
                    self.color_mode = ColorMode.SAME_COLOR
                else:
                    self.color_mode = ColorMode.DIFFERENT_COLORS
            elif event.key == pygame.K_SPACE:
                self.start_game()
    
    def start_game(self):
        """Начинает новую игру"""
        self.game_state = "game"
        self.score = 0
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.generate_new_expression()
        self.generate_numbers()
    
    def handle_game_events(self, event):
        """Обработка событий в игре"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.direction != (0, 1):
                self.direction = (0, -1)
            elif event.key == pygame.K_s and self.direction != (0, -1):
                self.direction = (0, 1)
            elif event.key == pygame.K_a and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif event.key == pygame.K_d and self.direction != (-1, 0):
                self.direction = (1, 0)
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
    
    def update_game(self):
        """Обновляет состояние игры"""
        if self.game_state != "game":
            return
        
        # Движение змейки
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Проверка столкновения со стенами
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or 
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_state = "game_over"
            return
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_state = "game_over"
            return
        
        self.snake.insert(0, new_head)
        
        # Проверка поедания числа
        eaten_number = None
        for i, (pos, number, is_correct) in enumerate(self.numbers_on_field):
            if new_head == pos:
                eaten_number = (i, number, is_correct)
                break
        
        if eaten_number:
            index, number, is_correct = eaten_number
            if is_correct:
                # Правильный ответ - змейка растёт
                self.score += 10
                self.generate_new_expression()
                self.generate_numbers()
            else:
                # Неправильный ответ - игра окончена
                self.game_state = "game_over"
                return
        else:
            # Обычное движение - убираем хвост
            self.snake.pop()
    
    def draw_menu(self):
        """Отрисовка меню"""
        self.screen.fill(BLACK)
        
        # Заголовок
        title = self.font.render("Математическая Змейка", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Операции
        y_offset = 120
        operations_title = self.small_font.render("Выберите операцию (1-5):", True, WHITE)
        self.screen.blit(operations_title, (50, y_offset))
        
        operations = [
            "1. Сложение (+)",
            "2. Вычитание (-)",
            "3. Умножение (*)",
            "4. Деление (/)",
            "5. Остаток от деления (%)"
        ]
        
        for i, op in enumerate(operations):
            color = GREEN if list(Operation)[i] == self.operation else WHITE
            text = self.small_font.render(op, True, color)
            self.screen.blit(text, (70, y_offset + 30 + i * 25))
        
        # Уровни сложности
        y_offset = 280
        difficulty_title = self.small_font.render("Выберите уровень сложности (Q,W,E,R,T):", True, WHITE)
        self.screen.blit(difficulty_title, (50, y_offset))
        
        difficulties = [
            "Q. " + Difficulty.LEVEL_1.value,
            "W. " + Difficulty.LEVEL_2.value,
            "E. " + Difficulty.LEVEL_3.value,
            "R. " + Difficulty.LEVEL_4.value,
            "T. " + Difficulty.LEVEL_5.value
        ]
        
        for i, diff in enumerate(difficulties):
            color = GREEN if list(Difficulty)[i] == self.difficulty else WHITE
            text = self.small_font.render(diff, True, color)
            self.screen.blit(text, (70, y_offset + 30 + i * 25))
        
        # Цветовой режим
        y_offset = 440
        color_title = self.small_font.render("Цветовой режим (C):", True, WHITE)
        self.screen.blit(color_title, (50, y_offset))
        
        color_text = f"C. {self.color_mode.value}"
        color_color = GREEN
        text = self.small_font.render(color_text, True, color_color)
        self.screen.blit(text, (70, y_offset + 25))
        
        # Инструкция для старта
        start_text = self.font.render("Нажмите ПРОБЕЛ для начала игры", True, YELLOW)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 540))
        self.screen.blit(start_text, start_rect)
    
    def draw_game(self):
        """Отрисовка игры"""
        self.screen.fill(BLACK)
        
        # Отрисовка выражения
        expr_text = self.font.render(self.current_expression, True, WHITE)
        expr_rect = expr_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(expr_text, expr_rect)
        
        # Отрисовка счёта
        score_text = self.small_font.render(f"Счёт: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Отрисовка змейки
        for segment in self.snake:
            rect = pygame.Rect(segment[0] * self.grid_size, segment[1] * self.grid_size, 
                             self.grid_size, self.grid_size)
            pygame.draw.rect(self.screen, GREEN, rect)
        
        # Отрисовка чисел на поле
        for pos, number, is_correct in self.numbers_on_field:
            rect = pygame.Rect(pos[0] * self.grid_size, pos[1] * self.grid_size, 
                             self.grid_size, self.grid_size)
            
            # Выбор цвета в зависимости от режима
            if self.color_mode == ColorMode.DIFFERENT_COLORS:
                color = BLUE if is_correct else RED
            else:  # SAME_COLOR
                color = BLUE  # Все числа одного цвета
                
            pygame.draw.rect(self.screen, color, rect)
            
            # Отрисовка числа
            num_text = self.number_font.render(str(number), True, WHITE)
            text_rect = num_text.get_rect(center=rect.center)
            self.screen.blit(num_text, text_rect)
        
        # Инструкция
        instr_text = self.small_font.render("ESC - в меню, WASD - управление", True, GRAY)
        self.screen.blit(instr_text, (10, WINDOW_HEIGHT - 25))
    
    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        self.screen.fill(BLACK)
        
        # Сообщение о проигрыше
        game_over_text = self.font.render("Игра окончена!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Счёт
        score_text = self.font.render(f"Ваш счёт: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # Инструкция для возврата в меню
        menu_text = self.small_font.render("Нажмите любую клавишу для возврата в меню", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
        self.screen.blit(menu_text, menu_rect)
    
    def run(self):
        """Основной игровой цикл"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.game_state == "menu":
                    self.handle_menu_events(event)
                elif self.game_state == "game":
                    self.handle_game_events(event)
                elif self.game_state == "game_over":
                    if event.type == pygame.KEYDOWN:
                        self.game_state = "menu"
            
            # Обновление игры
            self.update_game()
            
            # Отрисовка
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "game":
                self.draw_game()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(5)  # 5 FPS для змейки
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MathSnakeGame()
    game.run()
