import sys
import pygame
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from meteor import Meteor
import game_functions as gf
from button import Button

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Космическая одиссея")
    play_button = Button(settings, screen, 'Играть')
    stats = GameStats(settings)
    sb = Scoreboard(screen, settings, stats)

    # Создание корабля.
    ship = Ship(settings, screen)

    # Создание группы для хранения пуль.
    bullets = Group()
    # Создание группы для хранения метеоритов.
    meteors = Group()

    count = 0
    # Запуск основного цикла игры
    while True:
        gf.check_events(settings, screen, ship, bullets, stats, play_button, meteors, sb)
        gf.update_screen(settings, screen, ship, bullets, meteors, stats, play_button,sb)
        if stats.game_active:
            if count == 31:
                count = 0
            else:
                count += 1
            frame = count % 16

            bullets.update(frame)
            meteors.update()
            ship.update(settings)
            gf.update_meteors(settings, screen, ship, meteors, bullets, stats, sb)
            gf.update_bullets(settings, screen, ship, meteors, bullets, stats, sb)


run_game()