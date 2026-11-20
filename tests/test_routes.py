# УЧЕБНАЯ ВЕРСИЯ byVanoGame — tests/test_routes.py
# Автоматическая проверка игры. Тесты создают ситуации, выполняют действия и сравнивают результат с
# ожидаемым.
# Комментарии [исх. N] ссылаются на строку N обычной версии проекта и руководства Word. В этой копии
# номера редактора больше из-за пояснений.
# Python игнорирует строки с #. Код и строковые значения сохранены; сборка отдельно сравнивает
# синтаксическое дерево и значимые токены.

# [исх. 1] Строка документации объясняет назначение модуля, класса или функции; игровые действия здесь не
# выполняются.
"""Приёмочная проверка: пройти карты, а не расставить героя возле предметов."""
# [исх. 2] Подключаем unittest: стандартный запуск тестов и проверки ожидаемых результатов.
import unittest

# [исх. 4] Импортируем Commands из dormgame.commands.
from dormgame.commands import Commands
# [исх. 5] Импортируем FIXED_DT из dormgame.config.
from dormgame.config import FIXED_DT
# [исх. 6] Импортируем load_levels из dormgame.levels.
from dormgame.levels import load_levels
# [исх. 7] Импортируем GameSession из dormgame.model.
from dormgame.model import GameSession
# [исх. 8] Импортируем RouteController, measure_jump, verify_campaign из tools.verify_routes.
from tools.verify_routes import RouteController, measure_jump, verify_campaign


# [исх. 11] Объявляем класс RouteTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class RouteTests(unittest.TestCase):
    # МЕТОД RouteTests.test_entire_campaign_with_enemies_and_moving_platforms. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 12] Объявляем test_entire_campaign_with_enemies_and_moving_platforms: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_entire_campaign_with_enemies_and_moving_platforms(self):
        # [исх. 13] В results записываем результат: вызываем verify_campaign(); параметры названы в определении
        # этого метода.
        results = verify_campaign()
        # [исх. 14] Тест требует равенства фактического и ожидаемого результата у self; аргументы: [result.level
        # for result in results], [1, 2, 3].
        self.assertEqual([result.level for result in results], [1, 2, 3])
        # [исх. 15] Тест требует равенства фактического и ожидаемого результата у self; аргументы: [result.pages
        # for result in results], [4, 4, 5].
        self.assertEqual([result.pages for result in results], [4, 4, 5])
        # [исх. 16] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # sum((result.deaths for result in results)), 0.
        self.assertEqual(sum(result.deaths for result in results), 0)
        # [исх. 17] Тест требует, чтобы первое число было больше второго у self; аргументы: sum((result.jumps for
        # result in results)), 15.
        self.assertGreater(sum(result.jumps for result in results), 15)
        # [исх. 18] Тест требует, чтобы первое число было меньше второго у self; аргументы: sum((result.seconds
        # for result in results)), 120.
        self.assertLess(sum(result.seconds for result in results), 120)

    # МЕТОД RouteTests.test_optional_student_set_is_reachable_in_full_campaign. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 20] Объявляем test_optional_student_set_is_reachable_in_full_campaign: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_optional_student_set_is_reachable_in_full_campaign(self):
        # [исх. 21] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # sum((result.deaths for result in verify_campaign(True))), 0.
        self.assertEqual(sum(result.deaths for result in verify_campaign(True)), 0)

    # МЕТОД RouteTests.test_simulated_jump_supports_the_authored_platform_spacing. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 23] Объявляем test_simulated_jump_supports_the_authored_platform_spacing: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_simulated_jump_supports_the_authored_platform_spacing(self):
        # [исх. 24] В (height, distance) записываем результат: вызываем measure_jump(); параметры названы в
        # определении этого метода.
        height, distance = measure_jump()
        # Замер целой траектории выявляет регрессии порядка гравитации/прыжка;
        # карты используют подъёмы 32 px, а не предельные 55 px.
        # [исх. 27] Тест требует, чтобы первое число было больше второго у self; аргументы: height, 54.
        self.assertGreater(height, 54)
        # [исх. 28] Тест требует, чтобы первое число было меньше второго у self; аргументы: height, 57.
        self.assertLess(height, 57)
        # [исх. 29] Тест требует, чтобы первое число было больше второго у self; аргументы: distance, 105.
        self.assertGreater(distance, 105)
        # [исх. 30] Тест требует, чтобы первое число было меньше второго у self; аргументы: distance, 111.
        self.assertLess(distance, 111)

    # МЕТОД RouteTests.test_second_checkpoint_can_recover_missing_platform_page. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 32] Объявляем test_second_checkpoint_can_recover_missing_platform_page: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_second_checkpoint_can_recover_missing_platform_page(self):
        # [исх. 33] В session (сеанс прохождения всей игры) записываем результат: создаём новый сеанс прохождения
        # трёх этажей; аргументы: [load_levels()[1]].
        session = GameSession([load_levels()[1]])
        # [исх. 34] В control записываем результат: вызываем RouteController(session); параметры названы в
        # определении этого метода.
        control = RouteController(session)
        # [исх. 35] Вызываем control.walk(158); параметры названы в определении этого метода.
        control.walk(158)
        # [исх. 36] Вызываем control.jump(216); параметры названы в определении этого метода.
        control.jump(216)
        # [исх. 37] Вызываем control.walk(278); параметры названы в определении этого метода.
        control.walk(278)
        # [исх. 38] Вызываем control.jump(356); параметры названы в определении этого метода.
        control.jump(356)
        # [исх. 39] Вызываем control.walk(428); параметры названы в определении этого метода.
        control.walk(428)
        # [исх. 40] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # session.level.checkpoint_id, 'cp2'.
        self.assertEqual(session.level.checkpoint_id, 'cp2')
        # [исх. 41] Тест требует ложного условия у self; аргументы: session.level.pages[2].collected.
        self.assertFalse(session.level.pages[2].collected)
        # [исх. 42] Вызываем session.update(FIXED_DT, Commands(reset=True)); параметры названы в определении этого
        # метода.
        session.update(FIXED_DT, Commands(reset=True))
        # [исх. 43] Тест требует равенства фактического и ожидаемого результата у self; аргументы: session.deaths,
        # 1.
        self.assertEqual(session.deaths, 1)
        # [исх. 44] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # session.level.collected_pages, 2.
        self.assertEqual(session.level.collected_pages, 2)
        # [исх. 45] Вызываем control.walk(428); параметры названы в определении этого метода.
        control.walk(428)
        # [исх. 46] В platform (движущаяся грузовая платформа) записываем результат: элемент
        # session.level.platforms по индексу или ключу 0.
        platform = session.level.platforms[0]
        # [исх. 47] Вызываем control.wait_for(lambda: platform.box.x <= 494 and platform.dx < 0); параметры
        # названы в определении этого метода.
        control.wait_for(lambda: platform.box.x <= 494 and platform.dx < 0)
        # [исх. 48] Вызываем control.jump(lambda: platform.box.x + 25); параметры названы в определении этого
        # метода.
        control.jump(lambda: platform.box.x + 25)
        # [исх. 49] Вызываем control.wait_for(lambda: platform.box.x >= 542 and platform.dx > 0); параметры
        # названы в определении этого метода.
        control.wait_for(lambda: platform.box.x >= 542 and platform.dx > 0)
        # [исх. 50] Вызываем control.walk(580); параметры названы в определении этого метода.
        control.walk(580)
        # [исх. 51] Вызываем control.require_page('p3'); параметры названы в определении этого метода.
        control.require_page('p3')
        # [исх. 52] Тест требует равенства фактического и ожидаемого результата у self; аргументы: session.deaths,
        # 1.
        self.assertEqual(session.deaths, 1)


# [исх. 55] Проверяем: __name__ равно '__main__'. При успехе выполняется вложенный блок.
if __name__ == '__main__':
    # [исх. 56] Вызываем unittest.main(); параметры названы в определении этого метода.
    unittest.main()
