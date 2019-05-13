import sys
import pygame
from time import sleep
from bullet import Bullet
from meteor import Meteor

def check_events(settings, screen, ship, bullets, stats, play_button, meteors, sb):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button_on_mouse(settings, screen, stats, play_button, ship, bullets, meteors, mouse_x, mouse_y, sb)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
            # Начать перемещение корабля вправо
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
            # Начать перемещение корабля влево
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                # Создание новой пули и включение ее в группу bullets.
                if len(bullets) < settings.bullets_allowed:
                    new_bullet = Bullet(screen, ship)
                    bullets.add(new_bullet)

            elif event.key == pygame.K_RETURN:
                play_game(stats, meteors, bullets, ship, settings, sb)

            elif event.key == pygame.K_a:
                stats.game_active = False
                play_game(stats, meteors, bullets, ship, settings, sb)

            elif event.key == pygame.K_q:
                sys.exit()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
            # Закончить перемещение корабля вправо
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
            # Закончить перемещение корабля влево
                ship.moving_left = False


def play_game(stats, meteors, bullets, ship, settings, sb):
    """Запуск новой игры"""
    if stats.game_active == False:
        # Сброс игровой статистики
        stats.reset_stats()
        sb.reset_score()
        settings.initialize_dynamic_settings()
        meteors.empty()
        bullets.empty()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        ship.center_ship()
        stats.game_active = True
        pygame.mouse.set_visible(False)
        sleep(0.5)

def check_play_button_on_mouse(settings, screen, stats, play_button, ship, bullets, meteors, mouse_x, mouse_y, sb):
    """Запуск новой игры при нажатии кнопки 'Играть' мышкой"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        play_game(stats, meteors, bullets, ship, settings, sb)

def check_high_score(stats, sb):
    """Обновление рекордного счета"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def remove_bullets(bullets):
    """Удаление выстрелов, при достижении ими верхей точки окна"""
    if len(bullets) > 0:
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)


def add_meteors(settings, screen, meteors):
    """Добавление метеоритов"""
    if len(meteors) < settings.meteors_allowed:
        new_meteor = Meteor(screen)
        meteors.add(new_meteor)

def check_meteors_bottom(settings, screen, ship, meteors, bullets, stats, sb):
    """Уничтожение корабля при достижении метеоритом нижней точки окна"""
    screen_rect = screen.get_rect()
    for meteor in meteors.sprites():
        if meteor.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, meteors, bullets, sb)
            for meteor in meteors.copy():
                meteors.remove(meteor)
            break

def ship_hit(settings, stats, screen, ship, meteors, bullets, sb):
    """"Уничтожение корабля метеоритом"""
    meteors.empty()
    bullets.empty()
    sleep(0.5)
    ship.center_ship()
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        check_high_score(stats, sb)

def update_meteors(settings, screen, ship, meteors, bullets, stats, sb):
    """"Обновление метеоритов"""

    # Добавление метеорита
    add_meteors(settings, screen, meteors)

    # Вызов проверки на достижение метеоритом нижней точки окна
    check_meteors_bottom(settings, screen, ship, meteors, bullets, stats, sb)
    # Вызов проверки столкновения метеорита с кораблем
    check_ship_meteor_collisions(settings, stats, screen, ship, meteors, bullets, sb)


def update_bullets(settings, screen, ship, meteors, bullets, stats, sb):
    """Обновляет позиции пуль и уничтожение старых"""
    remove_bullets(bullets)
    check_bullet_meteor_collisions(bullets, meteors, settings, stats, sb)


def check_bullet_meteor_collisions(bullets, meteors, settings, stats, sb):
    # При столкновении выстрела и метеорита удаление обоих

    collisions = pygame.sprite.groupcollide(bullets, meteors, True, True)
    if collisions:
        settings.collisions_count += 1
        stats.score += settings.meteor_points
        sb.prep_score()
        if settings.collisions_count == 3:
            settings.increase_speed_points()
            stats.level += 1
            sb.prep_level()
            settings.collisions_count = 0

def check_ship_meteor_collisions(settings, stats, screen, ship, meteors, bullets, sb):
    # Вызов функции уничтожения корабля, при столкновении с метеоритом
    if pygame.sprite.spritecollideany(ship, meteors):
        ship_hit(settings, stats, screen, ship, meteors, bullets, sb)


def update_screen(settings, screen, ship, bullets, meteors, stats, play_button, sb):
    """Обновляет изображения на экране и отображает новый экран"""

    # Заполнение цветом фона
    screen.fill(settings.bg_color)

    # Вывод счета
    sb.show_score()

    # Прорисовывает кнопку "Играть", если игра не активна
    if not stats.game_active:
        play_button.draw_button()

    # Все пули выводятся позади изображений корабля
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Прорисовка метииоритов
    for meteor in meteors.sprites():
        meteor.draw_meteor()

    # При каждом проходе цикла перерисовывается экран.
    ship.blitme()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()
