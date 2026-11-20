# УЧЕБНАЯ ВЕРСИЯ byVanoGame — tests/test_model.py
# Автоматическая проверка игры. Тесты создают ситуации, выполняют действия и сравнивают результат с
# ожидаемым.
# Комментарии [исх. N] ссылаются на строку N обычной версии проекта и руководства Word. В этой копии
# номера редактора больше из-за пояснений.
# Python игнорирует строки с #. Код и строковые значения сохранены; сборка отдельно сравнивает
# синтаксическое дерево и значимые токены.

# [исх. 1] Строка документации объясняет назначение модуля, класса или функции; игровые действия здесь не
# выполняются.
"""Проверки правил сеанса: события, сохранение и полный цикл трёх карт."""
# [исх. 2] Подключаем copy: независимые копии данных для проверок, чтобы один тест не менял исходные карты.
import copy
# [исх. 3] Подключаем subprocess: запуск отдельного процесса Python для независимой проверки.
import subprocess
# [исх. 4] Подключаем sys: сведения о Python и пути импортов; полезны для проверки независимости модели от
# Pygame.
import sys
# [исх. 5] Подключаем unittest: стандартный запуск тестов и проверки ожидаемых результатов.
import unittest

# [исх. 7] Импортируем Commands из dormgame.commands.
from dormgame.commands import Commands
# [исх. 8] Импортируем FIXED_DT, RESPAWN_SHIELD из dormgame.config.
from dormgame.config import FIXED_DT, RESPAWN_SHIELD
# [исх. 9] Импортируем AABB из dormgame.geometry.
from dormgame.geometry import AABB
# [исх. 10] Импортируем load_levels, validate_level из dormgame.levels.
from dormgame.levels import load_levels, validate_level
# [исх. 11] Импортируем GameSession из dormgame.model.
from dormgame.model import GameSession


# [исх. 14] Объявляем класс ModelTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class ModelTests(unittest.TestCase):
    # МЕТОД ModelTests.setUp. unittest вызывает setUp перед каждым тестом: создаём свежие объекты, чтобы
    # проверки не зависели друг от друга.
    # Параметр self: текущий объект.
    # [исх. 15] Объявляем setUp: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в метод.
    def setUp(self):
        # [исх. 16] В self.game записываем результат: создаём новый сеанс прохождения трёх этажей.
        self.game = GameSession()

    # МЕТОД ModelTests.touch. Только тестовый помощник: ставит героя рядом с предметом для изолированной
    # проверки подбора. Контроллер полного маршрута так не делает.
    # Параметр self: текущий объект.
    # Параметр item: один предмет уровня.
    # [исх. 18] Объявляем touch: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в метод.
    def touch(self, item):
        # [исх. 19] В self.game.level.player.box.x (координата по горизонтали) записываем результат: item.box.x
        # (координата по горизонтали).
        self.game.level.player.box.x = item.box.x
        # [исх. 20] В self.game.level.player.box.y (координата по вертикали) записываем результат: разность в
        # формуле item.box.y - 4.
        self.game.level.player.box.y = item.box.y - 4
        # [исх. 21] В self.game.level.player.vy (скорость по Y в пикселях/с) записываем результат: число 0.0.
        self.game.level.player.vy = 0.0

    # МЕТОД ModelTests.test_page_collected_once_across_many_steps. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 23] Объявляем test_page_collected_once_across_many_steps: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_page_collected_once_across_many_steps(self):
        # [исх. 24] В page записываем результат: элемент self.game.level.pages по индексу или ключу 0.
        page = self.game.level.pages[0]
        # [исх. 25] Вызываем self.touch(page); параметры названы в определении этого метода.
        self.touch(page)
        # [исх. 26] Перебираем целые числа range(15); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(15):
            # [исх. 27] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого
            # метода.
            self.game.update(FIXED_DT, Commands())
        # [исх. 28] Тест требует истинного условия у self; аргументы: page.collected.
        self.assertTrue(page.collected)
        # [исх. 29] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.total_pages, 1.
        self.assertEqual(self.game.total_pages, 1)
        # [исх. 30] Тест требует равенства фактического и ожидаемого результата у self; аргументы: sum((e.kind ==
        # 'page' for e in self.game.drain_events())), 1.
        self.assertEqual(sum(e.kind == 'page' for e in self.game.drain_events()), 1)
        # [исх. 31] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.drain_events(), [].
        self.assertEqual(self.game.drain_events(), [])

    # МЕТОД ModelTests.test_optional_souvenir_is_unique_and_survives_respawn. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 33] Объявляем test_optional_souvenir_is_unique_and_survives_respawn: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_optional_souvenir_is_unique_and_survives_respawn(self):
        # [исх. 34] В souvenir записываем результат: элемент self.game.level.souvenirs по индексу или ключу 0.
        souvenir = self.game.level.souvenirs[0]
        # [исх. 35] Вызываем self.touch(souvenir); параметры названы в определении этого метода.
        self.touch(souvenir)
        # [исх. 36] Перебираем целые числа range(10); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(10):
            # [исх. 37] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого
            # метода.
            self.game.update(FIXED_DT, Commands())
        # [исх. 38] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.total_souvenirs, 1.
        self.assertEqual(self.game.total_souvenirs, 1)
        # [исх. 39] Тест требует равенства фактического и ожидаемого результата у self; аргументы: sum((e.kind ==
        # 'souvenir' for e in self.game.drain_events())), 1.
        self.assertEqual(sum(e.kind == 'souvenir' for e in self.game.drain_events()), 1)
        # [исх. 40] В self.game.level.reset_cooldown (оставшаяся задержка повторного R) записываем результат:
        # число 0.
        self.game.level.reset_cooldown = 0
        # [исх. 41] Вызываем self.game.update(FIXED_DT, Commands(reset=True)); параметры названы в определении
        # этого метода.
        self.game.update(FIXED_DT, Commands(reset=True))
        # [исх. 42] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.total_souvenirs, 1.
        self.assertEqual(self.game.total_souvenirs, 1)
        # [исх. 43] Вызываем self.game.new_game(); параметры названы в определении этого метода.
        self.game.new_game()
        # [исх. 44] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.total_souvenirs, 0.
        self.assertEqual(self.game.total_souvenirs, 0)

    # МЕТОД ModelTests.test_souvenirs_accumulate_across_levels_and_do_not_lock_exit. Проверочный
    # сценарий: подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 46] Объявляем test_souvenirs_accumulate_across_levels_and_do_not_lock_exit: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_souvenirs_accumulate_across_levels_and_do_not_lock_exit(self):
        # [исх. 47] Перебираем целые числа range(3); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в index, затем выполняется вложенный блок.
        for index in range(3):
            # [исх. 48] Вызываем self.touch(self.game.level.souvenirs[0]); параметры названы в определении этого
            # метода.
            self.touch(self.game.level.souvenirs[0])
            # [исх. 49] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого
            # метода.
            self.game.update(FIXED_DT, Commands())
            # [исх. 50] Перебираем self.game.level.pages (обязательные страницы). Очередной элемент записывается в
            # page, затем выполняется вложенный блок.
            for page in self.game.level.pages:
                # [исх. 51] В page.collected (подобран ли предмет) записываем результат: True — да, условие
                # выполнено.
                page.collected = True
            # [исх. 52] Вызываем self.touch(self.game.level.exit); параметры названы в определении этого метода.
            self.touch(self.game.level.exit)
            # [исх. 53] Вызываем self.game.update(FIXED_DT, Commands(interact=True)); параметры названы в
            # определении этого метода.
            self.game.update(FIXED_DT, Commands(interact=True))
            # [исх. 54] Вызываем self.game.advance_level(); параметры названы в определении этого метода.
            self.game.advance_level()
            # [исх. 55] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
            # self.game.total_souvenirs, index + 1.
            self.assertEqual(self.game.total_souvenirs, index + 1)
        # [исх. 56] Тест требует истинного условия у self; аргументы: self.game.finished.
        self.assertTrue(self.game.finished)
        # [исх. 57] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.souvenir_goal, 3.
        self.assertEqual(self.game.souvenir_goal, 3)

    # МЕТОД ModelTests.test_checkpoint_and_death_preserve_pages_reset_enemies_and_platforms. Проверочный
    # сценарий: подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 59] Объявляем test_checkpoint_and_death_preserve_pages_reset_enemies_and_platforms: тело ниже
    # выполнится при вызове. Отступы определяют, какие строки входят в метод.
    def test_checkpoint_and_death_preserve_pages_reset_enemies_and_platforms(self):
        # [исх. 60] В self.game.level.pages[0].collected (подобран ли предмет) записываем результат: True — да,
        # условие выполнено.
        self.game.level.pages[0].collected = True
        # [исх. 61] В checkpoint записываем результат: элемент self.game.level.checkpoints по индексу или ключу 0.
        checkpoint = self.game.level.checkpoints[0]
        # [исх. 62] Вызываем self.touch(checkpoint); параметры названы в определении этого метода.
        self.touch(checkpoint)
        # [исх. 63] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 64] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.level.checkpoint_id, checkpoint.id.
        self.assertEqual(self.game.level.checkpoint_id, checkpoint.id)
        # [исх. 65] Меняем self.game.level.enemies[0].box.x (координата по горизонтали): прибавляем число 30 и
        # сохраняем обратно.
        self.game.level.enemies[0].box.x += 30
        # [исх. 66] В self.game.level.reset_cooldown (оставшаяся задержка повторного R) записываем результат:
        # число 0.0.
        self.game.level.reset_cooldown = 0.0
        # [исх. 67] Вызываем self.game.update(FIXED_DT, Commands(reset=True)); параметры названы в определении
        # этого метода.
        self.game.update(FIXED_DT, Commands(reset=True))
        # [исх. 68] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.deaths, 1.
        self.assertEqual(self.game.deaths, 1)
        # [исх. 69] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.total_pages, 1.
        self.assertEqual(self.game.total_pages, 1)
        # [исх. 70] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.level.player.box.x, checkpoint.spawn[0].
        self.assertEqual(self.game.level.player.box.x, checkpoint.spawn[0])
        # [исх. 71] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.level.player.box.y, checkpoint.spawn[1].
        self.assertEqual(self.game.level.player.box.y, checkpoint.spawn[1])
        # [исх. 72] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.level.enemies[0].box.x, self.game.level.spec['enemies'][0]['x'].
        self.assertEqual(self.game.level.enemies[0].box.x, self.game.level.spec['enemies'][0]['x'])
        # [исх. 73] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.level.invulnerable, RESPAWN_SHIELD.
        self.assertEqual(self.game.level.invulnerable, RESPAWN_SHIELD)

    # МЕТОД ModelTests.test_reset_has_short_cooldown. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 75] Объявляем test_reset_has_short_cooldown: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_reset_has_short_cooldown(self):
        # [исх. 76] В self.game.level.reset_cooldown (оставшаяся задержка повторного R) записываем результат:
        # число 0.0.
        self.game.level.reset_cooldown = 0.0
        # [исх. 77] Вызываем self.game.update(FIXED_DT, Commands(reset=True)); параметры названы в определении
        # этого метода.
        self.game.update(FIXED_DT, Commands(reset=True))
        # [исх. 78] Перебираем целые числа range(20); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(20):
            # [исх. 79] Вызываем self.game.update(FIXED_DT, Commands(reset=True)); параметры названы в определении
            # этого метода.
            self.game.update(FIXED_DT, Commands(reset=True))
        # [исх. 80] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.deaths, 1.
        self.assertEqual(self.game.deaths, 1)

    # МЕТОД ModelTests.test_hazard_enemy_and_fall_each_cause_one_death. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 82] Объявляем test_hazard_enemy_and_fall_each_cause_one_death: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_hazard_enemy_and_fall_each_cause_one_death(self):
        # [исх. 83] В level (изменяемое состояние текущего этажа) записываем результат: self.game.level
        # (изменяемое состояние текущего этажа).
        level = self.game.level
        # [исх. 84] В level.invulnerable (оставшееся время защиты после появления) записываем результат: число
        # 0.0.
        level.invulnerable = 0.0
        # [исх. 85] Вызываем self.touch(level.hazards[0]); параметры названы в определении этого метода.
        self.touch(level.hazards[0])
        # [исх. 86] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 87] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.deaths, 1.
        self.assertEqual(self.game.deaths, 1)
        # [исх. 88] В level.invulnerable (оставшееся время защиты после появления) записываем результат: число
        # 0.0.
        level.invulnerable = 0.0
        # [исх. 89] Вызываем self.touch(level.enemies[0]); параметры названы в определении этого метода.
        self.touch(level.enemies[0])
        # [исх. 90] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 91] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.deaths, 2.
        self.assertEqual(self.game.deaths, 2)
        # [исх. 92] В level.player.box.y (координата по вертикали) записываем результат: сумма или объединение в
        # формуле level.height + 60.
        level.player.box.y = level.height + 60
        # [исх. 93] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 94] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.deaths, 3.
        self.assertEqual(self.game.deaths, 3)

    # МЕТОД ModelTests.test_spawn_shield_prevents_contact_repeat. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 96] Объявляем test_spawn_shield_prevents_contact_repeat: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_spawn_shield_prevents_contact_repeat(self):
        # [исх. 97] Вызываем self.touch(self.game.level.enemies[0]); параметры названы в определении этого метода.
        self.touch(self.game.level.enemies[0])
        # [исх. 98] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 99] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.deaths, 0.
        self.assertEqual(self.game.deaths, 0)

    # МЕТОД ModelTests.test_exit_closed_until_all_pages_collected. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 101] Объявляем test_exit_closed_until_all_pages_collected: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_exit_closed_until_all_pages_collected(self):
        # [исх. 102] В level (изменяемое состояние текущего этажа) записываем результат: self.game.level
        # (изменяемое состояние текущего этажа).
        level = self.game.level
        # [исх. 103] Вызываем self.touch(level.exit); параметры названы в определении этого метода.
        self.touch(level.exit)
        # [исх. 104] Вызываем self.game.update(FIXED_DT, Commands(interact=True)); параметры названы в определении
        # этого метода.
        self.game.update(FIXED_DT, Commands(interact=True))
        # [исх. 105] Тест требует ложного условия у self; аргументы: level.complete.
        self.assertFalse(level.complete)
        # [исх. 106] В events (накопленные сообщения о произошедшем) записываем результат: вызываем
        # self.game.drain_events(); параметры названы в определении этого метода.
        events = self.game.drain_events()
        # [исх. 107] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # events[-1].kind, 'locked'.
        self.assertEqual(events[-1].kind, 'locked')
        # [исх. 108] Тест требует наличие элемента в коллекции у self; аргументы: str(len(level.pages)),
        # events[-1].text.
        self.assertIn(str(len(level.pages)), events[-1].text)
        # [исх. 109] Перебираем level.pages (обязательные страницы). Очередной элемент записывается в page, затем
        # выполняется вложенный блок.
        for page in level.pages:
            # [исх. 110] В page.collected (подобран ли предмет) записываем результат: True — да, условие выполнено.
            page.collected = True
        # [исх. 111] Вызываем self.game.update(FIXED_DT, Commands(interact=True)); параметры названы в определении
        # этого метода.
        self.game.update(FIXED_DT, Commands(interact=True))
        # [исх. 112] Тест требует истинного условия у self; аргументы: level.complete.
        self.assertTrue(level.complete)

    # МЕТОД ModelTests.test_exit_requires_interaction. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 114] Объявляем test_exit_requires_interaction: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_exit_requires_interaction(self):
        # [исх. 115] Перебираем self.game.level.pages (обязательные страницы). Очередной элемент записывается в
        # page, затем выполняется вложенный блок.
        for page in self.game.level.pages:
            # [исх. 116] В page.collected (подобран ли предмет) записываем результат: True — да, условие выполнено.
            page.collected = True
        # [исх. 117] Вызываем self.touch(self.game.level.exit); параметры названы в определении этого метода.
        self.touch(self.game.level.exit)
        # [исх. 118] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 119] Тест требует ложного условия у self; аргументы: self.game.level.complete.
        self.assertFalse(self.game.level.complete)

    # МЕТОД ModelTests.test_note_interaction_produces_story. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 121] Объявляем test_note_interaction_produces_story: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_note_interaction_produces_story(self):
        # [исх. 122] В note записываем результат: элемент self.game.level.notes по индексу или ключу 0.
        note = self.game.level.notes[0]
        # [исх. 123] Вызываем self.touch(note); параметры названы в определении этого метода.
        self.touch(note)
        # [исх. 124] Вызываем self.game.update(FIXED_DT, Commands(interact=True)); параметры названы в определении
        # этого метода.
        self.game.update(FIXED_DT, Commands(interact=True))
        # [исх. 125] Тест требует истинного условия у self; аргументы: note.active.
        self.assertTrue(note.active)
        # [исх. 126] Тест требует наличие элемента в коллекции у self; аргументы: note.text, [e.text for e in
        # self.game.drain_events()].
        self.assertIn(note.text, [e.text for e in self.game.drain_events()])

    # МЕТОД ModelTests.test_pause_stops_all_timers_and_motion. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 128] Объявляем test_pause_stops_all_timers_and_motion: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_pause_stops_all_timers_and_motion(self):
        # [исх. 129] Вызываем self.game.update(FIXED_DT, Commands(move=1)); параметры названы в определении этого
        # метода.
        self.game.update(FIXED_DT, Commands(move=1))
        # [исх. 130] В before записываем результат: кортеж из 4 элементов, перечисленных ниже в коде.
        before = (self.game.elapsed, self.game.level.player.box.copy(),
                  # [исх. 131] Продолжение выражения выше: self.game.level.invulnerable (оставшееся время защиты
                  # после появления).
                  self.game.level.invulnerable, self.game.level.reset_cooldown)
        # [исх. 132] В self.game.paused (остановлены ли игровые правила) записываем результат: True — да, условие
        # выполнено.
        self.game.paused = True
        # [исх. 133] Перебираем целые числа range(100); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(100):
            # [исх. 134] Вызываем self.game.update(0.1, Commands(move=1, reset=True, jump_pressed=True)); параметры
            # названы в определении этого метода.
            self.game.update(0.1, Commands(move=1, reset=True, jump_pressed=True))
        # [исх. 135] В after записываем результат: кортеж из 4 элементов, перечисленных ниже в коде.
        after = (self.game.elapsed, self.game.level.player.box,
                 # [исх. 136] Продолжение выражения выше: self.game.level.invulnerable (оставшееся время защиты
                 # после появления).
                 self.game.level.invulnerable, self.game.level.reset_cooldown)
        # [исх. 137] Тест требует равенства фактического и ожидаемого результата у self; аргументы: before, after.
        self.assertEqual(before, after)

    # МЕТОД ModelTests.test_three_levels_final_statistics_and_new_game. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 139] Объявляем test_three_levels_final_statistics_and_new_game: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_three_levels_final_statistics_and_new_game(self):
        # [исх. 140] В expected_pages записываем результат: суммируем значения; True считается 1, False — 0;
        # аргументы: (len(s['pages']) for s in self.game.specs).
        expected_pages = sum(len(s['pages']) for s in self.game.specs)
        # [исх. 141] Перебираем целые числа range(3); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в index, затем выполняется вложенный блок.
        for index in range(3):
            # [исх. 142] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
            # self.game.level_index, index.
            self.assertEqual(self.game.level_index, index)
            # [исх. 143] Перебираем self.game.level.pages (обязательные страницы). Очередной элемент записывается в
            # page, затем выполняется вложенный блок.
            for page in self.game.level.pages:
                # [исх. 144] В page.collected (подобран ли предмет) записываем результат: True — да, условие
                # выполнено.
                page.collected = True
            # [исх. 145] Вызываем self.touch(self.game.level.exit); параметры названы в определении этого метода.
            self.touch(self.game.level.exit)
            # [исх. 146] Вызываем self.game.update(FIXED_DT, Commands(interact=True)); параметры названы в
            # определении этого метода.
            self.game.update(FIXED_DT, Commands(interact=True))
            # [исх. 147] Вызываем self.game.advance_level(); параметры названы в определении этого метода.
            self.game.advance_level()
        # [исх. 148] Тест требует истинного условия у self; аргументы: self.game.finished.
        self.assertTrue(self.game.finished)
        # [исх. 149] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.total_pages, expected_pages.
        self.assertEqual(self.game.total_pages, expected_pages)
        # [исх. 150] В final_time записываем результат: self.game.elapsed (игровое время в секундах).
        final_time = self.game.elapsed
        # [исх. 151] Вызываем self.game.update(FIXED_DT, Commands()); параметры названы в определении этого метода.
        self.game.update(FIXED_DT, Commands())
        # [исх. 152] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.elapsed, final_time.
        self.assertEqual(self.game.elapsed, final_time)
        # [исх. 153] Вызываем self.game.new_game(); параметры названы в определении этого метода.
        self.game.new_game()
        # [исх. 154] Тест требует ложного условия у self; аргументы: self.game.finished.
        self.assertFalse(self.game.finished)
        # [исх. 155] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # (self.game.level_index, self.game.total_pages, self.game.deaths, self.game.elapsed), (0, 0, 0,
        # 0.0).
        self.assertEqual((self.game.level_index, self.game.total_pages, self.game.deaths, self.game.elapsed), (0, 0, 0, 0.0))
        # [исх. 156] Тест требует именно отсутствия значения None у self; аргументы: self.game.level.checkpoint_id.
        self.assertIsNone(self.game.level.checkpoint_id)

    # МЕТОД ModelTests.test_cannot_advance_without_exit. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 158] Объявляем test_cannot_advance_without_exit: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_cannot_advance_without_exit(self):
        # [исх. 159] Вызываем self.game.advance_level(); параметры названы в определении этого метода.
        self.game.advance_level()
        # [исх. 160] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # self.game.level_index, 0.
        self.assertEqual(self.game.level_index, 0)

    # МЕТОД ModelTests.test_model_imports_without_pygame_or_site_packages. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 162] Объявляем test_model_imports_without_pygame_or_site_packages: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_model_imports_without_pygame_or_site_packages(self):
        # [исх. 163] В result записываем результат: вызываем subprocess.run([sys.executable, '-S', '-c', "import
        # sys; from dormgame.model import GameSession; GameSession(); assert 'pygame' not in
        # sys.modules"]); параметры названы в определении этого метода.
        result = subprocess.run([sys.executable, '-S', '-c',
                                 # [исх. 164] Продолжение выражения выше: текст "import sys; from dormgame.model
                                 # import GameSession; GameSession(); assert 'pygame' not in
                                 # sys.modules".
                                 "import sys; from dormgame.model import GameSession; GameSession(); assert 'pygame' not in sys.modules"],
                                # [исх. 165] Продолжение выражения выше: True — да, условие выполнено.
                                capture_output=True, text=True)
        # [исх. 166] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # result.returncode, 0, result.stderr.
        self.assertEqual(result.returncode, 0, result.stderr)


# [исх. 169] Объявляем класс LevelValidationTests: описание будущих объектов. Наследуем возможности
# unittest.TestCase.
class LevelValidationTests(unittest.TestCase):
    # МЕТОД LevelValidationTests.setUp. unittest вызывает setUp перед каждым тестом: создаём свежие
    # объекты, чтобы проверки не зависели друг от друга.
    # Параметр self: текущий объект.
    # [исх. 170] Объявляем setUp: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в метод.
    def setUp(self):
        # [исх. 171] В self.spec (словарь описания одного объекта или уровня из JSON) записываем результат:
        # вызываем copy.deepcopy(load_levels()[0]); параметры названы в определении этого метода.
        self.spec = copy.deepcopy(load_levels()[0])

    # МЕТОД LevelValidationTests.test_all_real_levels_valid. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 173] Объявляем test_all_real_levels_valid: тело ниже выполнится при вызове. Отступы определяют, какие
    # строки входят в метод.
    def test_all_real_levels_valid(self):
        # [исх. 174] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # len(load_levels()), 3.
        self.assertEqual(len(load_levels()), 3)

    # МЕТОД LevelValidationTests.test_start_and_exit_required. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 176] Объявляем test_start_and_exit_required: тело ниже выполнится при вызове. Отступы определяют, какие
    # строки входят в метод.
    def test_start_and_exit_required(self):
        # [исх. 177] Перебираем кортеж из 2 элементов, перечисленных ниже в коде. Очередной элемент записывается в
        # key, затем выполняется вложенный блок.
        for key in ('start', 'exit'):
            # [исх. 178] В spec (словарь описания одного объекта или уровня из JSON) записываем результат: вызываем
            # copy.deepcopy(self.spec); параметры названы в определении этого метода.
            spec = copy.deepcopy(self.spec)
            # [исх. 179] Выполняем конструкцию Delete; вложенные строки относятся к ней по отступу.
            del spec[key]
            # [исх. 180] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
            # исключение после выхода.
            with self.assertRaises(ValueError):
                # [исх. 181] Проверяем формат карты и безопасность размещения объектов; аргументы: spec.
                validate_level(spec)

    # МЕТОД LevelValidationTests.test_unique_ids_across_object_groups. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 183] Объявляем test_unique_ids_across_object_groups: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_unique_ids_across_object_groups(self):
        # [исх. 184] В self.spec['exit']['id'] записываем результат: элемент self.spec['pages'][0] по индексу или
        # ключу 'id'.
        self.spec['exit']['id'] = self.spec['pages'][0]['id']
        # [исх. 185] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with self.assertRaises(ValueError):
            # [исх. 186] Проверяем формат карты и безопасность размещения объектов; аргументы: self.spec.
            validate_level(self.spec)

    # МЕТОД LevelValidationTests.test_unknown_enemy_rejected. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 188] Объявляем test_unknown_enemy_rejected: тело ниже выполнится при вызове. Отступы определяют, какие
    # строки входят в метод.
    def test_unknown_enemy_rejected(self):
        # [исх. 189] В self.spec['enemies'][0]['kind'] записываем результат: текст 'dragon'.
        self.spec['enemies'][0]['kind'] = 'dragon'
        # [исх. 190] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with self.assertRaises(ValueError):
            # [исх. 191] Проверяем формат карты и безопасность размещения объектов; аргументы: self.spec.
            validate_level(self.spec)

    # МЕТОД LevelValidationTests.test_unknown_souvenir_and_duplicate_id_rejected. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 193] Объявляем test_unknown_souvenir_and_duplicate_id_rejected: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_unknown_souvenir_and_duplicate_id_rejected(self):
        # [исх. 194] Перебираем список из 2 элементов, перечисленных ниже в коде. Очередной элемент записывается в
        # (key, value), затем выполняется вложенный блок.
        for key, value in [('kind', 'unknown'), ('id', self.spec['pages'][0]['id'])]:
            # [исх. 195] В spec (словарь описания одного объекта или уровня из JSON) записываем результат: вызываем
            # copy.deepcopy(self.spec); параметры названы в определении этого метода.
            spec = copy.deepcopy(self.spec)
            # [исх. 196] В spec['souvenirs'][0][key] записываем результат: value (значение, которое текущий метод
            # проверяет, изменяет или выводит).
            spec['souvenirs'][0][key] = value
            # [исх. 197] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
            # исключение после выхода.
            with self.assertRaises(ValueError):
                # [исх. 198] Проверяем формат карты и безопасность размещения объектов; аргументы: spec.
                validate_level(spec)

    # МЕТОД LevelValidationTests.test_outside_invalid_size_nan_and_wrong_type. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 200] Объявляем test_outside_invalid_size_nan_and_wrong_type: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_outside_invalid_size_nan_and_wrong_type(self):
        # [исх. 201] Перебираем кортеж из 5 элементов, перечисленных ниже в коде. Очередной элемент записывается в
        # rect, затем выполняется вложенный блок.
        for rect in ([0, 0, -1, 8], [2000, 0, 8, 8], [0, float('nan'), 8, 8], 'bad', [False, 0, 8, 8]):
            # [исх. 202] В spec (словарь описания одного объекта или уровня из JSON) записываем результат: вызываем
            # copy.deepcopy(self.spec); параметры названы в определении этого метода.
            spec = copy.deepcopy(self.spec)
            # [исх. 203] В spec['pages'][0]['rect'] записываем результат: rect (прямоугольник).
            spec['pages'][0]['rect'] = rect
            # [исх. 204] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
            # исключение после выхода.
            with self.assertRaises(ValueError):
                # [исх. 205] Проверяем формат карты и безопасность размещения объектов; аргументы: spec.
                validate_level(spec)

    # МЕТОД LevelValidationTests.test_start_inside_wall_rejected. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 207] Объявляем test_start_inside_wall_rejected: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_start_inside_wall_rejected(self):
        # [исх. 208] В self.spec['start'] записываем результат: список из 2 элементов, перечисленных ниже в коде.
        self.spec['start'] = [40, 430]
        # [исх. 209] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with self.assertRaises(ValueError):
            # [исх. 210] Проверяем формат карты и безопасность размещения объектов; аргументы: self.spec.
            validate_level(self.spec)

    # МЕТОД LevelValidationTests.test_enemy_start_inside_wall_rejected. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 212] Объявляем test_enemy_start_inside_wall_rejected: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_enemy_start_inside_wall_rejected(self):
        # [исх. 213] Вызываем self.spec['enemies'][0].update(); параметры названы в определении этого метода.
        self.spec['enemies'][0].update(x=220, y=390, left=180, right=330)
        # [исх. 214] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with self.assertRaises(ValueError):
            # [исх. 215] Проверяем формат карты и безопасность размещения объектов; аргументы: self.spec.
            validate_level(self.spec)

    # МЕТОД LevelValidationTests.test_platform_path_crossing_static_wall_rejected. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 217] Объявляем test_platform_path_crossing_static_wall_rejected: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_platform_path_crossing_static_wall_rejected(self):
        # [исх. 218] В self.spec['platforms'] записываем результат: список из 1 элементов, перечисленных ниже в
        # коде.
        self.spec['platforms'] = [{'id': 'invalid', 'rect': [10, 390, 20, 8],
                                  # [исх. 219] Продолжение выражения выше: текст 'end'.
                                  'end': [400, 390], 'speed': 25}]
        # [исх. 220] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with self.assertRaises(ValueError):
            # [исх. 221] Проверяем формат карты и безопасность размещения объектов; аргументы: self.spec.
            validate_level(self.spec)


# [исх. 224] Проверяем: __name__ равно '__main__'. При успехе выполняется вложенный блок.
if __name__ == '__main__':
    # [исх. 225] Вызываем unittest.main(); параметры названы в определении этого метода.
    unittest.main()
