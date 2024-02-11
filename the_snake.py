from random import randint
from typing import List, Tuple
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject():
    """Абстрактный класс будущих игровых объектов"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=SNAKE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный клас для отрисовки"""
        pass


class Snake(GameObject):
    """Класс описывающий змею"""

    body_color = (0, 255, 0)
    next_direction = None
    positions: List[Tuple[int, int]] = []
    last = None

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 direction=RIGHT):
        super().__init__(position, self.body_color)
        self.length = 1
        self.positions.append(position)
        self.direction = direction

    def update_direction(self):
        """Обновление направления движение головы змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещение головы змеи(путём добавления
        в список нового элемента)
        """
        head = self.get_head_position()
        self.positions.append(((head[0] + self.direction[0] * GRID_SIZE)
                               % SCREEN_WIDTH, (head[1] + self.direction[1]
                                                * GRID_SIZE) % SCREEN_HEIGHT))
        if self.positions[-1] in self.positions[:-1]:
            self.reset()

    def draw(self, surface):
        """Отрисовка змеи"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        # Добовление новой головы по текущему направлению
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Метод для получения координат головы змеи"""
        return self.positions[-1]

    def reset(self):
        """Перезапуск игры"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        screen.fill(BOARD_BACKGROUND_COLOR)
        pass


class Apple(GameObject):
    """Класс для игрового объекта - яблочка"""

    body_color = (255, 0, 0)

    def __init__(self):
        super().__init__(None, self.body_color)
        self.randomize_position()

    def randomize_position(self):
        """Выдаём яблочку случайную позицию."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Функция отрисовки яблока"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def main():
    """Логика игрового процесса : главный игровой цикл"""
    snake = Snake((320, 240), (-1, 0))
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            print("apple")
            snake.length += 1
            apple.randomize_position()
            print(snake.length)
        if snake.length == len(snake.positions) - 2:
            snake.last = snake.positions.pop(0)
        print(snake.positions)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
