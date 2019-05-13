import pygame
from pygame.sprite import Sprite
import spritesheet
from settings import Settings

class Bullet(Sprite):
    """Класс для управления пулями, выпущенными кораблем."""
    def __init__(self, screen, ship):
        settings = Settings()
        super(Bullet, self).__init__()
        self.screen = screen

        # Создание пули в позиции (0,0) и назначение правильной позиции.
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.ss = spritesheet.spritesheet("images/bullet_ss.gif")
        self.images = self.ss.load_strip((0, 0, settings.bullet_width, settings.bullet_height), 16)
        self.image = self.images[0]

        # Позиция пули хранится в вещественном формате.
        self.y = float(self.rect.y)
        # self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor
        self.frame = 0
        self.iteration = 0

    def update(self, frame):
        """Перемещает пулю вверх по экрану."""
        # Обновление позиции пули в вещественном формате.
        self.y -= self.speed_factor

        # Обновление позиции прямоугольника.
        self.rect.y = self.y
        # Анимация пули
        self.image = self.images[self.frame]

        # Ограничиваем кол-во фреймов
        if self.frame == 15:
            self.frame = 0

        # Меняем фрейм каждую n итерацию основного цикла
        if self.iteration%4 == 0:
            self.frame += 1

        self.iteration += 1
        # Ограничиваем макс. число в счетчике итераций для защиты от переполнения
        if self.iteration == 64:
            self.iteration = 0


    def draw_bullet(self):
        """Вывод пули на экран."""
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)