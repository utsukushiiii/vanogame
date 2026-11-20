# УЧЕБНАЯ ВЕРСИЯ byVanoGame — tests/test_physics.py
# Автоматическая проверка игры. Тесты создают ситуации, выполняют действия и сравнивают результат с
# ожидаемым.
# Комментарии [исх. N] ссылаются на строку N обычной версии проекта и руководства Word. В этой копии
# номера редактора больше из-за пояснений.
# Python игнорирует строки с #. Код и строковые значения сохранены; сборка отдельно сравнивает
# синтаксическое дерево и значимые токены.

# [исх. 1] Строка документации объясняет назначение модуля, класса или функции; игровые действия здесь не
# выполняются.
"""Регрессии физики без Pygame, окна и реального времени."""
# [исх. 2] Подключаем unittest: стандартный запуск тестов и проверки ожидаемых результатов.
import unittest

# [исх. 4] Импортируем config из dormgame.
from dormgame import config
# [исх. 5] Импортируем Commands из dormgame.commands.
from dormgame.commands import Commands
# [исх. 6] Импортируем AABB из dormgame.geometry.
from dormgame.geometry import AABB
# [исх. 7] Импортируем Body, MovingPlatform, PlayerBody, SpatialGrid, move_body, update_player из
# dormgame.physics.
from dormgame.physics import Body, MovingPlatform, PlayerBody, SpatialGrid, move_body, update_player


# [исх. 10] Объявляем класс CollisionTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class CollisionTests(unittest.TestCase):
    # МЕТОД CollisionTests.test_landing_stops_at_floor_and_sets_grounded. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 11] Объявляем test_landing_stops_at_floor_and_sets_grounded: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_landing_stops_at_floor_and_sets_grounded(self):
        # [исх. 12] В body (физическое тело с прямоугольником и скоростями) записываем результат: создаём
        # физическое тело с прямоугольником и начальными скоростями; аргументы: AABB(5, 0, 10, 10).
        body = Body(AABB(5, 0, 10, 10), vy=150)
        # [исх. 13] В result записываем результат: применяем смещение тела с осевыми проверками стен; аргументы:
        # body, 0, 55, SpatialGrid([AABB(0, 40, 100, 8)]).
        result = move_body(body, 0, 55, SpatialGrid([AABB(0, 40, 100, 8)]))
        # [исх. 14] Тест требует истинного условия у self; аргументы: result.landed.
        self.assertTrue(result.landed)
        # [исх. 15] Тест требует истинного условия у self; аргументы: body.grounded.
        self.assertTrue(body.grounded)
        # [исх. 16] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # body.box.bottom, 40.
        self.assertEqual(body.box.bottom, 40)
        # [исх. 17] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.vy, 0.
        self.assertEqual(body.vy, 0)

    # МЕТОД CollisionTests.test_wall_stops_horizontal_motion_without_losing_height. Проверочный
    # сценарий: подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 19] Объявляем test_wall_stops_horizontal_motion_without_losing_height: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_wall_stops_horizontal_motion_without_losing_height(self):
        # [исх. 20] В body (физическое тело с прямоугольником и скоростями) записываем результат: создаём
        # физическое тело с прямоугольником и начальными скоростями; аргументы: AABB(0, 5, 10, 10).
        body = Body(AABB(0, 5, 10, 10), vx=100)
        # [исх. 21] В result записываем результат: применяем смещение тела с осевыми проверками стен; аргументы:
        # body, 60, 0, SpatialGrid([AABB(30, 0, 8, 100)]).
        result = move_body(body, 60, 0, SpatialGrid([AABB(30, 0, 8, 100)]))
        # [исх. 22] Тест требует истинного условия у self; аргументы: result.hit_x.
        self.assertTrue(result.hit_x)
        # [исх. 23] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.box.right,
        # 30.
        self.assertEqual(body.box.right, 30)
        # [исх. 24] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.box.y, 5.
        self.assertEqual(body.box.y, 5)
        # [исх. 25] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.vx, 0.
        self.assertEqual(body.vx, 0)

    # МЕТОД CollisionTests.test_ceiling_clears_upward_speed. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 27] Объявляем test_ceiling_clears_upward_speed: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_ceiling_clears_upward_speed(self):
        # [исх. 28] В body (физическое тело с прямоугольником и скоростями) записываем результат: создаём
        # физическое тело с прямоугольником и начальными скоростями; аргументы: AABB(5, 40, 10, 10).
        body = Body(AABB(5, 40, 10, 10), vy=-200)
        # [исх. 29] В result записываем результат: применяем смещение тела с осевыми проверками стен; аргументы:
        # body, 0, -70, SpatialGrid([AABB(0, 10, 100, 4)]).
        result = move_body(body, 0, -70, SpatialGrid([AABB(0, 10, 100, 4)]))
        # [исх. 30] Тест требует истинного условия у self; аргументы: result.ceiling.
        self.assertTrue(result.ceiling)
        # [исх. 31] Тест требует ложного условия у self; аргументы: body.grounded.
        self.assertFalse(body.grounded)
        # [исх. 32] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.box.top,
        # 14.
        self.assertEqual(body.box.top, 14)
        # [исх. 33] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.vy, 0.
        self.assertEqual(body.vy, 0)

    # МЕТОД CollisionTests.test_max_speed_cannot_tunnel_through_subpixel_platform. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 35] Объявляем test_max_speed_cannot_tunnel_through_subpixel_platform: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_max_speed_cannot_tunnel_through_subpixel_platform(self):
        # [исх. 36] В body (физическое тело с прямоугольником и скоростями) записываем результат: создаём
        # физическое тело с прямоугольником и начальными скоростями; аргументы: AABB(5, 0, 10, 10).
        body = Body(AABB(5, 0, 10, 10), vy=config.MAX_FALL_SPEED)
        # [исх. 37] В floor записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина,
        # высота; аргументы: 0, 23.123, 60, 0.1.
        floor = AABB(0, 23.123, 60, 0.1)
        # [исх. 38] В result записываем результат: применяем смещение тела с осевыми проверками стен; аргументы:
        # body, 0, config.MAX_FALL_SPEED * 0.1, SpatialGrid([floor]).
        result = move_body(body, 0, config.MAX_FALL_SPEED * 0.1, SpatialGrid([floor]))
        # [исх. 39] Тест требует истинного условия у self; аргументы: result.landed.
        self.assertTrue(result.landed)
        # [исх. 40] Тест сравнивает дробные числа с допуском округления у self; аргументы: body.box.bottom,
        # floor.top.
        self.assertAlmostEqual(body.box.bottom, floor.top)

    # МЕТОД CollisionTests.test_diagonal_corner_stays_outside_walls. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 42] Объявляем test_diagonal_corner_stays_outside_walls: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_diagonal_corner_stays_outside_walls(self):
        # [исх. 43] В walls записываем результат: список из 2 элементов, перечисленных ниже в коде.
        walls = [AABB(40, 0, 8, 100), AABB(0, 60, 100, 8)]
        # [исх. 44] В body (физическое тело с прямоугольником и скоростями) записываем результат: создаём
        # физическое тело с прямоугольником и начальными скоростями; аргументы: AABB(15, 15, 10, 10).
        body = Body(AABB(15, 15, 10, 10))
        # [исх. 45] Применяем смещение тела с осевыми проверками стен; аргументы: body, 100, 100,
        # SpatialGrid(walls).
        move_body(body, 100, 100, SpatialGrid(walls))
        # [исх. 46] Тест требует равенства фактического и ожидаемого результата у self; аргументы: body.box.right,
        # 40.
        self.assertEqual(body.box.right, 40)
        # [исх. 47] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # body.box.bottom, 60.
        self.assertEqual(body.box.bottom, 60)
        # [исх. 48] Тест требует ложного условия у self; аргументы: any((body.box.intersects(wall) for wall in
        # walls)).
        self.assertFalse(any(body.box.intersects(wall) for wall in walls))

    # МЕТОД CollisionTests.test_spatial_index_deduplicates_and_supports_negative_cells. Проверочный
    # сценарий: подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 50] Объявляем test_spatial_index_deduplicates_and_supports_negative_cells: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_spatial_index_deduplicates_and_supports_negative_cells(self):
        # [исх. 51] В large записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина,
        # высота; аргументы: -40, -30, 100, 100.
        large = AABB(-40, -30, 100, 100)
        # [исх. 52] В far записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 500, 0, 10, 10.
        far = AABB(500, 0, 10, 10)
        # [исх. 53] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [large, far], 16.
        grid = SpatialGrid([large, far], 16)
        # [исх. 54] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # grid.query(AABB(-20, -20, 40, 40)), [large].
        self.assertEqual(grid.query(AABB(-20, -20, 40, 40)), [large])


# [исх. 57] Объявляем класс JumpTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class JumpTests(unittest.TestCase):
    # МЕТОД JumpTests.setUp. unittest вызывает setUp перед каждым тестом: создаём свежие объекты, чтобы
    # проверки не зависели друг от друга.
    # Параметр self: текущий объект.
    # [исх. 58] Объявляем setUp: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в метод.
    def setUp(self):
        # [исх. 59] В self.dt (длительность одного обновления в секундах) записываем результат: config.FIXED_DT.
        self.dt = config.FIXED_DT
        # [исх. 60] В self.floor записываем результат: строим индекс неподвижных стен для быстрых локальных
        # запросов; аргументы: [AABB(-100, 100, 500, 10)].
        self.floor = SpatialGrid([AABB(-100, 100, 500, 10)])
        # [исх. 61] В self.player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(0, 74, 16, 26).
        self.player = PlayerBody(AABB(0, 74, 16, 26))
        # [исх. 62] Выполняем физический шаг героя и получаем события; аргументы: self.player, Commands(),
        # self.dt, self.floor, [].
        update_player(self.player, Commands(), self.dt, self.floor, [])

    # МЕТОД JumpTests.test_coyote_jump_after_leaving_edge. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 64] Объявляем test_coyote_jump_after_leaving_edge: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_coyote_jump_after_leaving_edge(self):
        # [исх. 65] В self.player.box.x (координата по горизонтали) записываем результат: число 420.
        self.player.box.x = 420
        # [исх. 66] Перебираем целые числа range(8); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(8):
            # [исх. 67] Выполняем физический шаг героя и получаем события; аргументы: self.player, Commands(),
            # self.dt, self.floor, [].
            update_player(self.player, Commands(), self.dt, self.floor, [])
        # [исх. 68] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический шаг
        # героя и получаем события; аргументы: self.player, Commands(jump_pressed=True, jump_held=True),
        # self.dt, self.floor, [].
        events = update_player(self.player, Commands(jump_pressed=True, jump_held=True),
                               # [исх. 69] Продолжение выражения выше: self.dt (длительность одного обновления в
                               # секундах).
                               self.dt, self.floor, [])
        # [исх. 70] Тест требует наличие элемента в коллекции у self; аргументы: 'jump', events.
        self.assertIn("jump", events)
        # [исх. 71] Тест требует, чтобы первое число было меньше второго у self; аргументы: self.player.vy, -250.
        self.assertLess(self.player.vy, -250)

    # МЕТОД JumpTests.test_coyote_expires. Проверочный сценарий: подготовка ситуации, действие,
    # сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 73] Объявляем test_coyote_expires: тело ниже выполнится при вызове. Отступы определяют, какие строки
    # входят в метод.
    def test_coyote_expires(self):
        # [исх. 74] В self.player.box.x (координата по горизонтали) записываем результат: число 420.
        self.player.box.x = 420
        # [исх. 75] Перебираем целые числа range(16); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(16):
            # [исх. 76] Выполняем физический шаг героя и получаем события; аргументы: self.player, Commands(),
            # self.dt, self.floor, [].
            update_player(self.player, Commands(), self.dt, self.floor, [])
        # [исх. 77] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический шаг
        # героя и получаем события; аргументы: self.player, Commands(jump_pressed=True, jump_held=True),
        # self.dt, self.floor, [].
        events = update_player(self.player, Commands(jump_pressed=True, jump_held=True),
                               # [исх. 78] Продолжение выражения выше: self.dt (длительность одного обновления в
                               # секундах).
                               self.dt, self.floor, [])
        # [исх. 79] Тест требует отсутствие элемента у self; аргументы: 'jump', events.
        self.assertNotIn("jump", events)
        # [исх. 80] Тест требует, чтобы первое число было больше второго у self; аргументы: self.player.vy, 0.
        self.assertGreater(self.player.vy, 0)

    # МЕТОД JumpTests.test_jump_buffer_consumed_on_landing. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 82] Объявляем test_jump_buffer_consumed_on_landing: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_jump_buffer_consumed_on_landing(self):
        # [исх. 83] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(0, 52, 16, 26).
        player = PlayerBody(AABB(0, 52, 16, 26), vy=280)
        # [исх. 84] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический шаг
        # героя и получаем события; аргументы: player, Commands(jump_pressed=True, jump_held=True),
        # self.dt, self.floor, [].
        events = update_player(player, Commands(jump_pressed=True, jump_held=True),
                               # [исх. 85] Продолжение выражения выше: self.dt (длительность одного обновления в
                               # секундах).
                               self.dt, self.floor, [])
        # [исх. 86] Перебираем целые числа range(10); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(10):
            # [исх. 87] Меняем events (накопленные сообщения о произошедшем): прибавляем выполняем физический шаг
            # героя и получаем события; аргументы: player, Commands(jump_held=True), self.dt,
            # self.floor, [] и сохраняем обратно.
            events += update_player(player, Commands(jump_held=True), self.dt, self.floor, [])
        # [исх. 88] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # events.count('jump'), 1.
        self.assertEqual(events.count("jump"), 1)
        # [исх. 89] Тест требует наличие элемента в коллекции у self; аргументы: 'land', events.
        self.assertIn("land", events)
        # [исх. 90] Тест требует, чтобы первое число было меньше второго у self; аргументы: player.vy, 0.
        self.assertLess(player.vy, 0)

    # МЕТОД JumpTests.test_expired_buffer_does_not_jump_on_landing. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 92] Объявляем test_expired_buffer_does_not_jump_on_landing: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_expired_buffer_does_not_jump_on_landing(self):
        # [исх. 93] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(0, 0, 16, 26).
        player = PlayerBody(AABB(0, 0, 16, 26))
        # [исх. 94] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический шаг
        # героя и получаем события; аргументы: player, Commands(jump_pressed=True, jump_held=True),
        # self.dt, self.floor, [].
        events = update_player(player, Commands(jump_pressed=True, jump_held=True),
                               # [исх. 95] Продолжение выражения выше: self.dt (длительность одного обновления в
                               # секундах).
                               self.dt, self.floor, [])
        # [исх. 96] Перебираем целые числа range(100); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(100):
            # [исх. 97] Меняем events (накопленные сообщения о произошедшем): прибавляем выполняем физический шаг
            # героя и получаем события; аргументы: player, Commands(jump_held=True), self.dt,
            # self.floor, [] и сохраняем обратно.
            events += update_player(player, Commands(jump_held=True), self.dt, self.floor, [])
        # [исх. 98] Тест требует отсутствие элемента у self; аргументы: 'jump', events.
        self.assertNotIn("jump", events)
        # [исх. 99] Тест требует истинного условия у self; аргументы: player.grounded.
        self.assertTrue(player.grounded)

    # МЕТОД JumpTests.test_holding_after_one_press_never_repeats_jump. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 101] Объявляем test_holding_after_one_press_never_repeats_jump: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_holding_after_one_press_never_repeats_jump(self):
        # [исх. 102] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический шаг
        # героя и получаем события; аргументы: self.player, Commands(jump_pressed=True, jump_held=True),
        # self.dt, self.floor, [].
        events = update_player(self.player, Commands(jump_pressed=True, jump_held=True),
                               # [исх. 103] Продолжение выражения выше: self.dt (длительность одного обновления в
                               # секундах).
                               self.dt, self.floor, [])
        # [исх. 104] Перебираем целые числа range(240); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(240):
            # [исх. 105] Меняем events (накопленные сообщения о произошедшем): прибавляем выполняем физический шаг
            # героя и получаем события; аргументы: self.player, Commands(jump_held=True), self.dt,
            # self.floor, [] и сохраняем обратно.
            events += update_player(self.player, Commands(jump_held=True), self.dt, self.floor, [])
        # [исх. 106] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # events.count('jump'), 1.
        self.assertEqual(events.count("jump"), 1)
        # [исх. 107] Тест требует истинного условия у self; аргументы: self.player.grounded.
        self.assertTrue(self.player.grounded)

    # МЕТОД JumpTests.test_early_release_reduces_jump_height. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 109] Объявляем test_early_release_reduces_jump_height: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_early_release_reduces_jump_height(self):
        # МЕТОД JumpTests.test_early_release_reduces_jump_height.apex. Вспомогательная функция проверки;
        # действия подробно разобраны ниже.
        # Параметр hold_steps: входное значение; использование показано в строках тела.
        # [исх. 110] Объявляем apex: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в
        # метод.
        def apex(hold_steps):
            # [исх. 111] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
            # аргументы: AABB(0, 74, 16, 26).
            player = PlayerBody(AABB(0, 74, 16, 26))
            # [исх. 112] В top (вертикальная координата начала панели) записываем результат: player.box.y
            # (координата по вертикали).
            top = player.box.y
            # [исх. 113] Перебираем целые числа range(120); правая граница не включается, третий аргумент задаёт
            # шаг. Очередной элемент записывается в step, затем выполняется вложенный блок.
            for step in range(120):
                # [исх. 114] Выполняем физический шаг героя и получаем события; аргументы: player,
                # Commands(jump_pressed=step == 0, jump_held=step < hold_steps), self.dt, self.floor,
                # [].
                update_player(player, Commands(jump_pressed=step == 0, jump_held=step < hold_steps),
                              # [исх. 115] Продолжение выражения выше: self.dt (длительность одного обновления в
                              # секундах).
                              self.dt, self.floor, [])
                # [исх. 116] В top (вертикальная координата начала панели) записываем результат: выбираем
                # минимальное значение; аргументы: top, player.box.y.
                top = min(top, player.box.y)
            # [исх. 117] Завершаем этот вызов и возвращаем вызывающему коду: top (вертикальная координата начала
            # панели).
            return top
        # [исх. 118] Тест требует, чтобы первое число было меньше второго у self; аргументы: apex(100), apex(4) -
        # 15.
        self.assertLess(apex(100), apex(4) - 15)

    # МЕТОД JumpTests.test_stationary_grounded_does_not_emit_repeated_landings. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 120] Объявляем test_stationary_grounded_does_not_emit_repeated_landings: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_stationary_grounded_does_not_emit_repeated_landings(self):
        # [исх. 121] В events (накопленные сообщения о произошедшем) записываем результат: пустой список.
        events = []
        # [исх. 122] Перебираем целые числа range(120); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(120):
            # [исх. 123] Меняем events (накопленные сообщения о произошедшем): прибавляем выполняем физический шаг
            # героя и получаем события; аргументы: self.player, Commands(), self.dt, self.floor, [] и
            # сохраняем обратно.
            events += update_player(self.player, Commands(), self.dt, self.floor, [])
        # [исх. 124] Тест требует равенства фактического и ожидаемого результата у self; аргументы: events, [].
        self.assertEqual(events, [])
        # [исх. 125] Тест требует истинного условия у self; аргументы: self.player.grounded.
        self.assertTrue(self.player.grounded)


# [исх. 128] Объявляем класс PlatformTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class PlatformTests(unittest.TestCase):
    # МЕТОД PlatformTests.test_horizontal_platform_carries_passenger. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 129] Объявляем test_horizontal_platform_carries_passenger: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_horizontal_platform_carries_passenger(self):
        # [исх. 130] В platform (движущаяся грузовая платформа) записываем результат: вызываем
        # MovingPlatform('lift', AABB(0, 100, 60, 8), (120, 100), 45); параметры названы в определении
        # этого метода.
        platform = MovingPlatform("lift", AABB(0, 100, 60, 8), (120, 100), 45)
        # [исх. 131] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(15, 74, 16, 26).
        player = PlayerBody(AABB(15, 74, 16, 26), grounded=True, support_id="lift")
        # [исх. 132] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [].
        grid = SpatialGrid([])
        # [исх. 133] Перебираем целые числа range(60); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(60):
            # [исх. 134] Вызываем platform.update(config.FIXED_DT); параметры названы в определении этого метода.
            platform.update(config.FIXED_DT)
            # [исх. 135] Тест требует отсутствие элемента у self; аргументы: 'crushed', update_player(player,
            # Commands(), config.FIXED_DT, grid, [platform]).
            self.assertNotIn("crushed", update_player(player, Commands(), config.FIXED_DT, grid, [platform]))
        # [исх. 136] Тест сравнивает дробные числа с допуском округления у self; аргументы: player.box.x, 37.5.
        self.assertAlmostEqual(player.box.x, 37.5)
        # [исх. 137] Тест сравнивает дробные числа с допуском округления у self; аргументы: player.box.bottom,
        # platform.box.top.
        self.assertAlmostEqual(player.box.bottom, platform.box.top)
        # [исх. 138] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # player.support_id, 'lift'.
        self.assertEqual(player.support_id, "lift")

    # МЕТОД PlatformTests.test_vertical_platform_carries_passenger. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 140] Объявляем test_vertical_platform_carries_passenger: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_vertical_platform_carries_passenger(self):
        # [исх. 141] В platform (движущаяся грузовая платформа) записываем результат: вызываем
        # MovingPlatform('lift', AABB(0, 100, 60, 8), (0, 40), 30); параметры названы в определении
        # этого метода.
        platform = MovingPlatform("lift", AABB(0, 100, 60, 8), (0, 40), 30)
        # [исх. 142] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(15, 74, 16, 26).
        player = PlayerBody(AABB(15, 74, 16, 26), grounded=True, support_id="lift")
        # [исх. 143] Перебираем целые числа range(60); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(60):
            # [исх. 144] Вызываем platform.update(config.FIXED_DT); параметры названы в определении этого метода.
            platform.update(config.FIXED_DT)
            # [исх. 145] Тест требует отсутствие элемента у self; аргументы: 'crushed', update_player(player,
            # Commands(), config.FIXED_DT, SpatialGrid([]), [platform]).
            self.assertNotIn("crushed", update_player(player, Commands(), config.FIXED_DT,
                                                     # [исх. 146] Продолжение выражения выше: строим индекс неподвижных
                                                     # стен для быстрых локальных запросов; аргументы: [].
                                                     SpatialGrid([]), [platform]))
        # [исх. 147] Тест сравнивает дробные числа с допуском округления у self; аргументы: player.box.bottom, 85.
        self.assertAlmostEqual(player.box.bottom, 85)
        # [исх. 148] Тест требует истинного условия у self; аргументы: player.grounded.
        self.assertTrue(player.grounded)

    # МЕТОД PlatformTests.test_jump_detaches_without_platform_drag. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 150] Объявляем test_jump_detaches_without_platform_drag: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_jump_detaches_without_platform_drag(self):
        # [исх. 151] В platform (движущаяся грузовая платформа) записываем результат: вызываем
        # MovingPlatform('lift', AABB(0, 100, 60, 8), (120, 100), 45); параметры названы в определении
        # этого метода.
        platform = MovingPlatform("lift", AABB(0, 100, 60, 8), (120, 100), 45)
        # [исх. 152] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(15, 74, 16, 26).
        player = PlayerBody(AABB(15, 74, 16, 26), grounded=True, support_id="lift")
        # [исх. 153] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [].
        grid = SpatialGrid([])
        # [исх. 154] Вызываем platform.update(config.FIXED_DT); параметры названы в определении этого метода.
        platform.update(config.FIXED_DT)
        # [исх. 155] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический шаг
        # героя и получаем события; аргументы: player, Commands(jump_pressed=True, jump_held=True),
        # config.FIXED_DT, grid, [platform].
        events = update_player(player, Commands(jump_pressed=True, jump_held=True),
                               # [исх. 156] Продолжение выражения выше: config.FIXED_DT.
                               config.FIXED_DT, grid, [platform])
        # [исх. 157] Тест требует наличие элемента в коллекции у self; аргументы: 'jump', events.
        self.assertIn("jump", events)
        # [исх. 158] Тест требует именно отсутствия значения None у self; аргументы: player.support_id.
        self.assertIsNone(player.support_id)
        # [исх. 159] Тест требует равенства фактического и ожидаемого результата у self; аргументы: player.box.x,
        # 15.
        self.assertEqual(player.box.x, 15)
        # [исх. 160] Перебираем целые числа range(10); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(10):
            # [исх. 161] Вызываем platform.update(config.FIXED_DT); параметры названы в определении этого метода.
            platform.update(config.FIXED_DT)
            # [исх. 162] Выполняем физический шаг героя и получаем события; аргументы: player,
            # Commands(jump_held=True), config.FIXED_DT, grid, [platform].
            update_player(player, Commands(jump_held=True), config.FIXED_DT, grid, [platform])
        # [исх. 163] Тест требует равенства фактического и ожидаемого результата у self; аргументы: player.box.x,
        # 15.
        self.assertEqual(player.box.x, 15)
        # [исх. 164] Тест требует, чтобы первое число было меньше второго у self; аргументы: player.box.bottom,
        # platform.box.top.
        self.assertLess(player.box.bottom, platform.box.top)

    # МЕТОД PlatformTests.test_upward_platform_under_ceiling_emits_crush. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 166] Объявляем test_upward_platform_under_ceiling_emits_crush: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_upward_platform_under_ceiling_emits_crush(self):
        # [исх. 167] В platform (движущаяся грузовая платформа) записываем результат: вызываем
        # MovingPlatform('lift', AABB(0, 100, 60, 8), (0, 0), 60); параметры названы в определении этого
        # метода.
        platform = MovingPlatform("lift", AABB(0, 100, 60, 8), (0, 0), 60)
        # [исх. 168] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(15, 74, 16, 26).
        player = PlayerBody(AABB(15, 74, 16, 26), grounded=True, support_id="lift")
        # [исх. 169] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [AABB(-10, 50, 100, 10)].
        grid = SpatialGrid([AABB(-10, 50, 100, 10)])
        # [исх. 170] В events (накопленные сообщения о произошедшем) записываем результат: пустой список.
        events = []
        # [исх. 171] Перебираем целые числа range(40); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(40):
            # [исх. 172] Вызываем platform.update(config.FIXED_DT); параметры названы в определении этого метода.
            platform.update(config.FIXED_DT)
            # [исх. 173] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический
            # шаг героя и получаем события; аргументы: player, Commands(), config.FIXED_DT, grid,
            # [platform].
            events = update_player(player, Commands(), config.FIXED_DT, grid, [platform])
            # [исх. 174] Проверяем: 'crushed' содержится в events. При успехе выполняется вложенный блок.
            if "crushed" in events:
                # [исх. 175] Полностью выходим из ближайшего цикла; выполнение продолжается после него.
                break
        # [исх. 176] Тест требует наличие элемента в коллекции у self; аргументы: 'crushed', events.
        self.assertIn("crushed", events)
        # [исх. 177] Тест требует, чтобы первое число было не меньше второго у self; аргументы: player.box.top, 60.
        self.assertGreaterEqual(player.box.top, 60)

    # МЕТОД PlatformTests.test_platform_pushes_from_side_and_crushes_against_wall. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 179] Объявляем test_platform_pushes_from_side_and_crushes_against_wall: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_platform_pushes_from_side_and_crushes_against_wall(self):
        # [исх. 180] В platform (движущаяся грузовая платформа) записываем результат: вызываем
        # MovingPlatform('pusher', AABB(0, 50, 20, 60), (150, 50), 120); параметры названы в определении
        # этого метода.
        platform = MovingPlatform("pusher", AABB(0, 50, 20, 60), (150, 50), 120)
        # [исх. 181] В player (тело героя) записываем результат: создаём тело героя, включая таймеры прыжка;
        # аргументы: AABB(24, 74, 16, 26).
        player = PlayerBody(AABB(24, 74, 16, 26), grounded=True)
        # [исх. 182] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [AABB(0, 100, 200, 8), AABB(55, 0,
        # 8, 100)].
        grid = SpatialGrid([AABB(0, 100, 200, 8), AABB(55, 0, 8, 100)])
        # [исх. 183] В events (накопленные сообщения о произошедшем) записываем результат: пустой список.
        events = []
        # [исх. 184] Перебираем целые числа range(50); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(50):
            # [исх. 185] Вызываем platform.update(config.FIXED_DT); параметры названы в определении этого метода.
            platform.update(config.FIXED_DT)
            # [исх. 186] В events (накопленные сообщения о произошедшем) записываем результат: выполняем физический
            # шаг героя и получаем события; аргументы: player, Commands(), config.FIXED_DT, grid,
            # [platform].
            events = update_player(player, Commands(), config.FIXED_DT, grid, [platform])
            # [исх. 187] Проверяем: 'crushed' содержится в events. При успехе выполняется вложенный блок.
            if "crushed" in events:
                # [исх. 188] Полностью выходим из ближайшего цикла; выполнение продолжается после него.
                break
        # [исх. 189] Тест требует наличие элемента в коллекции у self; аргументы: 'crushed', events.
        self.assertIn("crushed", events)
        # [исх. 190] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # player.box.right, 55.
        self.assertEqual(player.box.right, 55)

    # МЕТОД PlatformTests.test_platform_pingpong_handles_endpoint_and_resets. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 192] Объявляем test_platform_pingpong_handles_endpoint_and_resets: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_platform_pingpong_handles_endpoint_and_resets(self):
        # [исх. 193] В platform (движущаяся грузовая платформа) записываем результат: вызываем
        # MovingPlatform('lift', AABB(0, 10, 60, 8), (100, 10), 100); параметры названы в определении
        # этого метода.
        platform = MovingPlatform("lift", AABB(0, 10, 60, 8), (100, 10), 100)
        # [исх. 194] Вызываем platform.update(1.25); параметры названы в определении этого метода.
        platform.update(1.25)
        # [исх. 195] Тест сравнивает дробные числа с допуском округления у self; аргументы: platform.box.x, 75.
        self.assertAlmostEqual(platform.box.x, 75)
        # [исх. 196] Вызываем platform.update(0.5); параметры названы в определении этого метода.
        platform.update(0.5)
        # [исх. 197] Тест сравнивает дробные числа с допуском округления у self; аргументы: platform.box.x, 25.
        self.assertAlmostEqual(platform.box.x, 25)
        # [исх. 198] Тест сравнивает дробные числа с допуском округления у self; аргументы: platform.dx, -50.
        self.assertAlmostEqual(platform.dx, -50)
        # [исх. 199] Вызываем platform.reset(); параметры названы в определении этого метода.
        platform.reset()
        # [исх. 200] Тест требует равенства фактического и ожидаемого результата у self; аргументы: platform.box.x,
        # 0.
        self.assertEqual(platform.box.x, 0)
        # [исх. 201] Тест требует равенства фактического и ожидаемого результата у self; аргументы: platform.dx, 0.
        self.assertEqual(platform.dx, 0)


# [исх. 204] Проверяем: __name__ равно '__main__'. При успехе выполняется вложенный блок.
if __name__ == "__main__":
    # [исх. 205] Вызываем unittest.main(); параметры названы в определении этого метода.
    unittest.main()
