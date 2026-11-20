# УЧЕБНАЯ ВЕРСИЯ byVanoGame — tests/test_enemies.py
# Автоматическая проверка игры. Тесты создают ситуации, выполняют действия и сравнивают результат с
# ожидаемым.
# Комментарии [исх. N] ссылаются на строку N обычной версии проекта и руководства Word. В этой копии
# номера редактора больше из-за пояснений.
# Python игнорирует строки с #. Код и строковые значения сохранены; сборка отдельно сравнивает
# синтаксическое дерево и значимые токены.

# [исх. 1] Подключаем unittest: стандартный запуск тестов и проверки ожидаемых результатов.
import unittest
# [исх. 2] Импортируем patch из unittest.mock.
from unittest.mock import patch

# [исх. 4] Импортируем config из dormgame.
from dormgame import config
# [исх. 5] Импортируем DroneEnemy, Enemy, PatrolEnemy, build_enemy из dormgame.enemies.
from dormgame.enemies import DroneEnemy, Enemy, PatrolEnemy, build_enemy
# [исх. 6] Импортируем AABB из dormgame.geometry.
from dormgame.geometry import AABB
# [исх. 7] Импортируем SpatialGrid из dormgame.physics.
from dormgame.physics import SpatialGrid


# [исх. 10] Объявляем класс EnemyTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class EnemyTests(unittest.TestCase):
    # МЕТОД EnemyTests.test_enemy_contract_is_abstract. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 11] Объявляем test_enemy_contract_is_abstract: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_enemy_contract_is_abstract(self):
        # [исх. 12] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with self.assertRaises(TypeError):
            # [исх. 13] Вызываем Enemy('abstract', AABB(0, 0, 18, 14)); параметры названы в определении этого
            # метода.
            Enemy("abstract", AABB(0, 0, 18, 14))

    # МЕТОД EnemyTests.test_factory_uses_common_lifecycle. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 15] Объявляем test_factory_uses_common_lifecycle: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_factory_uses_common_lifecycle(self):
        # [исх. 16] В specs (описания всех уровней) записываем результат: список из 2 элементов, перечисленных
        # ниже в коде.
        specs = [
            # [исх. 17] Продолжение выражения выше: словарь из 6 элементов, перечисленных ниже в коде.
            {"id": "guard", "kind": "patrol", "x": 32, "y": 80,
             # [исх. 18] Продолжение выражения выше: текст 'left'.
             "left": 16, "right": 160},
            # [исх. 19] Продолжение выражения выше: словарь из 5 элементов, перечисленных ниже в коде.
            {"id": "drone", "kind": "drone", "x": 48, "y": 48,
             # [исх. 20] Продолжение выражения выше: текст 'route'.
             "route": [[56, 56], [136, 56]]},
        # [исх. 21] Закрываем скобки многострочной конструкции выше; отдельного нового действия эта строка не
        # запускает.
        ]
        # [исх. 22] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [].
        grid = SpatialGrid([])
        # [исх. 23] Перебираем specs (описания всех уровней). Очередной элемент записывается в spec, затем
        # выполняется вложенный блок.
        for spec in specs:
            # [исх. 24] В enemy записываем результат: выбираем класс врага по полю kind и создаём его; аргументы:
            # spec, [], 320, 240.
            enemy = build_enemy(spec, [], 320, 240)
            # [исх. 25] Вызываем self.assertIsInstance(enemy, Enemy); параметры названы в определении этого
            # метода.
            self.assertIsInstance(enemy, Enemy)
            # [исх. 26] Вызываем self.assertIsInstance(enemy.update(0.01, AABB(300, 200, 16, 26), grid), list);
            # параметры названы в определении этого метода.
            self.assertIsInstance(enemy.update(.01, AABB(300, 200, 16, 26), grid), list)
            # [исх. 27] Вызываем enemy.reset(); параметры названы в определении этого метода.
            enemy.reset()
            # [исх. 28] Тест требует равенства фактического и ожидаемого результата у self; аргументы: enemy.age,
            # 0.
            self.assertEqual(enemy.age, 0)
            # [исх. 29] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
            # enemy.state, 'Патруль'.
            self.assertEqual(enemy.state, "Патруль")

    # МЕТОД EnemyTests.test_drone_chases_around_wall_without_any_intersection. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 31] Объявляем test_drone_chases_around_wall_without_any_intersection: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_drone_chases_around_wall_without_any_intersection(self):
        # [исх. 32] В wall записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 176, 64, 16, 176.
        wall = AABB(176, 64, 16, 176)
        # [исх. 33] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [wall].
        grid = SpatialGrid([wall])
        # [исх. 34] В drone записываем результат: вызываем DroneEnemy('test', AABB(95, 145, 18, 14), [(104, 152)],
        # [wall], 400, 240); параметры названы в определении этого метода.
        drone = DroneEnemy("test", AABB(95, 145, 18, 14), [(104, 152)],
                           # [исх. 35] Продолжение выражения выше: список из 1 элементов, перечисленных ниже в
                           # коде.
                           [wall], 400, 240)
        # [исх. 36] В player (тело героя) записываем результат: создаём дробный прямоугольник с аргументами x, y,
        # ширина, высота; аргументы: 240, 140, 16, 26.
        player = AABB(240, 140, 16, 26)
        # [исх. 37] В detected записываем результат: число 0.
        detected = 0
        # [исх. 38] В visited_above_wall записываем результат: False — нет, условие не выполнено.
        visited_above_wall = False
        # [исх. 39] Перебираем целые числа range(1200); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(1200):
            # [исх. 40] Меняем detected: прибавляем вызываем drone.update(config.FIXED_DT, player,
            # grid).count('detected'); параметры названы в определении этого метода и сохраняем обратно.
            detected += drone.update(config.FIXED_DT, player, grid).count("detected")
            # [исх. 41] Тест требует ложного условия у self; аргументы: drone.box.intersects(wall).
            self.assertFalse(drone.box.intersects(wall))
            # [исх. 42] Меняем visited_above_wall: применяем операцию с drone.box.bottom не больше wall.top и
            # сохраняем обратно.
            visited_above_wall |= drone.box.bottom <= wall.top
        # [исх. 43] Тест требует равенства фактического и ожидаемого результата у self; аргументы: detected, 1.
        self.assertEqual(detected, 1)
        # [исх. 44] Тест требует истинного условия у self; аргументы: visited_above_wall.
        self.assertTrue(visited_above_wall)
        # [исх. 45] Тест требует, чтобы первое число было больше второго у self; аргументы: drone.box.left,
        # wall.right.
        self.assertGreater(drone.box.left, wall.right)
        # [исх. 46] Тест требует, чтобы первое число было больше второго у self; аргументы: drone.expanded, 0.
        self.assertGreater(drone.expanded, 0)
        # [исх. 47] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.state,
        # DroneEnemy.CHASE.
        self.assertEqual(drone.state, DroneEnemy.CHASE)

    # МЕТОД EnemyTests.test_drone_state_machine_and_predictable_reset. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 49] Объявляем test_drone_state_machine_and_predictable_reset: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_drone_state_machine_and_predictable_reset(self):
        # [исх. 50] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [].
        grid = SpatialGrid([])
        # [исх. 51] В drone записываем результат: вызываем DroneEnemy('test', AABB(55, 65, 18, 14), [(56, 72),
        # (216, 72)], [], 640, 240); параметры названы в определении этого метода.
        drone = DroneEnemy("test", AABB(55, 65, 18, 14), [(56, 72), (216, 72)],
                           # [исх. 52] Продолжение выражения выше: пустой список.
                           [], 640, 240)
        # [исх. 53] В spawn (точка появления героя) записываем результат: создаём отдельную копию у drone.box.
        spawn = drone.box.copy()
        # [исх. 54] В near (расстояние до преграждающей поверхности) записываем результат: создаём дробный
        # прямоугольник с аргументами x, y, ширина, высота; аргументы: 140, 62, 16, 26.
        near = AABB(140, 62, 16, 26)
        # [исх. 55] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # drone.update(0.01, near, grid), ['detected'].
        self.assertEqual(drone.update(.01, near, grid), ["detected"])
        # [исх. 56] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # drone.update(0.01, near, grid), [].
        self.assertEqual(drone.update(.01, near, grid), [])
        # [исх. 57] Перебираем целые числа range(120); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(120):
            # [исх. 58] Вызываем drone.update(config.FIXED_DT, near, grid); параметры названы в определении этого
            # метода.
            drone.update(config.FIXED_DT, near, grid)
        # [исх. 59] В far записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 600, 190, 16, 26.
        far = AABB(600, 190, 16, 26)
        # [исх. 60] Вызываем drone.update(config.FIXED_DT, far, grid); параметры названы в определении этого
        # метода.
        drone.update(config.FIXED_DT, far, grid)
        # [исх. 61] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.state,
        # DroneEnemy.RETURN.
        self.assertEqual(drone.state, DroneEnemy.RETURN)
        # [исх. 62] Перебираем целые числа range(600); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(600):
            # [исх. 63] Вызываем drone.update(config.FIXED_DT, far, grid); параметры названы в определении этого
            # метода.
            drone.update(config.FIXED_DT, far, grid)
        # [исх. 64] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.state,
        # DroneEnemy.PATROL.
        self.assertEqual(drone.state, DroneEnemy.PATROL)
        # [исх. 65] Вызываем drone.reset(); параметры названы в определении этого метода.
        drone.reset()
        # [исх. 66] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.box,
        # spawn.
        self.assertEqual(drone.box, spawn)
        # [исх. 67] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.path, [].
        self.assertEqual(drone.path, [])
        # [исх. 68] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.state,
        # DroneEnemy.PATROL.
        self.assertEqual(drone.state, DroneEnemy.PATROL)

    # МЕТОД EnemyTests.test_drone_does_not_recalculate_every_step. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 70] Объявляем test_drone_does_not_recalculate_every_step: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_drone_does_not_recalculate_every_step(self):
        # [исх. 71] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [].
        grid = SpatialGrid([])
        # [исх. 72] В drone записываем результат: вызываем DroneEnemy('test', AABB(55, 65, 18, 14), [(216, 72)],
        # [], 640, 240); параметры названы в определении этого метода.
        drone = DroneEnemy("test", AABB(55, 65, 18, 14), [(216, 72)], [], 640, 240)
        # [исх. 73] В original записываем результат: drone._find_path.
        original = drone._find_path
        # [исх. 74] В searches записываем результат: пустой список.
        searches = []

        # МЕТОД EnemyTests.test_drone_does_not_recalculate_every_step.counting_search. Вспомогательная
        # функция проверки; действия подробно разобраны ниже.
        # Параметр target: целевое значение или точка назначения по контексту.
        # [исх. 76] Объявляем counting_search: тело ниже выполнится при вызове. Отступы определяют, какие строки
        # входят в метод.
        def counting_search(target):
            # [исх. 77] Добавляем один элемент в конец у searches; аргументы: target.
            searches.append(target)
            # [исх. 78] Вызываем original(target); параметры названы в определении этого метода.
            original(target)

        # [исх. 80] В drone._find_path записываем результат: counting_search.
        drone._find_path = counting_search
        # [исх. 81] Перебираем целые числа range(120); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(120):
            # [исх. 82] Вызываем drone.update(config.FIXED_DT, AABB(600, 190, 16, 26), grid); параметры названы в
            # определении этого метода.
            drone.update(config.FIXED_DT, AABB(600, 190, 16, 26), grid)
        # [исх. 83] Тест требует, чтобы первое число было не меньше второго у self; аргументы: len(searches), 2.
        self.assertGreaterEqual(len(searches), 2)
        # [исх. 84] Тест требует, чтобы первое число было не больше второго у self; аргументы: len(searches), 3.
        self.assertLessEqual(len(searches), 3)

    # МЕТОД EnemyTests.test_drone_cannot_cross_disconnected_wall_even_with_large_dt. Проверочный
    # сценарий: подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 86] Объявляем test_drone_cannot_cross_disconnected_wall_even_with_large_dt: тело ниже выполнится при
    # вызове. Отступы определяют, какие строки входят в метод.
    def test_drone_cannot_cross_disconnected_wall_even_with_large_dt(self):
        # [исх. 87] В wall записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 128, 0, 2, 192.
        wall = AABB(128, 0, 2, 192)
        # [исх. 88] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [wall].
        grid = SpatialGrid([wall])
        # [исх. 89] В drone записываем результат: вызываем DroneEnemy('test', AABB(47, 81, 18, 14), [(56, 88)],
        # [wall], 320, 192); параметры названы в определении этого метода.
        drone = DroneEnemy("test", AABB(47, 81, 18, 14), [(56, 88)],
                           # [исх. 90] Продолжение выражения выше: список из 1 элементов, перечисленных ниже в
                           # коде.
                           [wall], 320, 192)
        # [исх. 91] В player (тело героя) записываем результат: создаём дробный прямоугольник с аргументами x, y,
        # ширина, высота; аргументы: 168, 81, 16, 26.
        player = AABB(168, 81, 16, 26)
        # [исх. 92] Перебираем целые числа range(20); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(20):
            # [исх. 93] Вызываем drone.update(1.0, player, grid); параметры названы в определении этого метода.
            drone.update(1.0, player, grid)
            # [исх. 94] Тест требует ложного условия у self; аргументы: drone.box.intersects(wall).
            self.assertFalse(drone.box.intersects(wall))
            # [исх. 95] Тест требует, чтобы первое число было не больше второго у self; аргументы:
            # drone.box.right, wall.left.
            self.assertLessEqual(drone.box.right, wall.left)

    # МЕТОД EnemyTests.test_drone_no_navigation_space_is_safe. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 97] Объявляем test_drone_no_navigation_space_is_safe: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_drone_no_navigation_space_is_safe(self):
        # [исх. 98] В wall записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 0, 0, 64, 64.
        wall = AABB(0, 0, 64, 64)
        # [исх. 99] В drone записываем результат: вызываем DroneEnemy('test', AABB(5, 5, 18, 14), [], [wall], 64,
        # 64); параметры названы в определении этого метода.
        drone = DroneEnemy("test", AABB(5, 5, 18, 14), [], [wall], 64, 64)
        # [исх. 100] Вызываем drone.update(0.1, AABB(50, 50, 10, 10), SpatialGrid([wall])); параметры названы в
        # определении этого метода.
        drone.update(.1, AABB(50, 50, 10, 10), SpatialGrid([wall]))
        # [исх. 101] Тест требует равенства фактического и ожидаемого результата у self; аргументы: drone.path, [].
        self.assertEqual(drone.path, [])

    # МЕТОД EnemyTests.test_no_path_still_respects_repath_interval. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 103] Объявляем test_no_path_still_respects_repath_interval: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_no_path_still_respects_repath_interval(self):
        # [исх. 104] В wall записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 0, 0, 64, 64.
        wall = AABB(0, 0, 64, 64)
        # [исх. 105] В drone записываем результат: вызываем DroneEnemy('blocked', AABB(5, 5, 18, 14), [], [wall],
        # 64, 64); параметры названы в определении этого метода.
        drone = DroneEnemy('blocked', AABB(5, 5, 18, 14), [], [wall], 64, 64)
        # [исх. 106] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with patch.object(drone, '_find_path', wraps=drone._find_path) as search:
            # [исх. 107] Перебираем целые числа range(120); правая граница не включается, третий аргумент задаёт
            # шаг. Очередной элемент записывается в _, затем выполняется вложенный блок.
            for _ in range(120):
                # [исх. 108] Вызываем drone.update(config.FIXED_DT, AABB(500, 500, 16, 26), SpatialGrid([wall]));
                # параметры названы в определении этого метода.
                drone.update(config.FIXED_DT, AABB(500, 500, 16, 26), SpatialGrid([wall]))
            # [исх. 109] Тест требует, чтобы первое число было не меньше второго у self; аргументы:
            # search.call_count, 2.
            self.assertGreaterEqual(search.call_count, 2)
            # [исх. 110] Тест требует, чтобы первое число было не больше второго у self; аргументы:
            # search.call_count, 3.
            self.assertLessEqual(search.call_count, 3)

    # МЕТОД EnemyTests.test_patrol_turns_before_wall_and_ledge. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 112] Объявляем test_patrol_turns_before_wall_and_ledge: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_patrol_turns_before_wall_and_ledge(self):
        # [исх. 113] В floor записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина,
        # высота; аргументы: 0, 100, 220, 20.
        floor = AABB(0, 100, 220, 20)
        # [исх. 114] В wall записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина, высота;
        # аргументы: 150, 40, 16, 60.
        wall = AABB(150, 40, 16, 60)
        # [исх. 115] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [floor, wall].
        grid = SpatialGrid([floor, wall])
        # [исх. 116] В guard записываем результат: вызываем PatrolEnemy('test', AABB(60, 74, 18, 26), 0, 220);
        # параметры названы в определении этого метода.
        guard = PatrolEnemy("test", AABB(60, 74, 18, 26), 0, 220)
        # [исх. 117] В (positions, directions) записываем результат: кортеж из 2 элементов, перечисленных ниже в
        # коде.
        positions, directions = [], set()
        # [исх. 118] Перебираем целые числа range(1800); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(1800):
            # [исх. 119] Вызываем guard.update(config.FIXED_DT, AABB(300, 200, 16, 26), grid); параметры названы в
            # определении этого метода.
            guard.update(config.FIXED_DT, AABB(300, 200, 16, 26), grid)
            # [исх. 120] Тест требует ложного условия у self; аргументы: guard.box.intersects(floor).
            self.assertFalse(guard.box.intersects(floor))
            # [исх. 121] Тест требует ложного условия у self; аргументы: guard.box.intersects(wall).
            self.assertFalse(guard.box.intersects(wall))
            # [исх. 122] Тест сравнивает дробные числа с допуском округления у self; аргументы: guard.box.bottom,
            # floor.top.
            self.assertAlmostEqual(guard.box.bottom, floor.top)
            # [исх. 123] Добавляем один элемент в конец у positions; аргументы: guard.box.x.
            positions.append(guard.box.x)
            # [исх. 124] Добавляем элемент в множество без повторов у directions; аргументы: guard.facing.
            directions.add(guard.facing)
        # [исх. 125] Тест требует равенства фактического и ожидаемого результата у self; аргументы: directions,
        # {-1, 1}.
        self.assertEqual(directions, {-1, 1})
        # [исх. 126] Тест требует, чтобы первое число было не меньше второго у self; аргументы: min(positions), 0.
        self.assertGreaterEqual(min(positions), 0)
        # [исх. 127] Тест требует, чтобы первое число было не больше второго у self; аргументы: max(positions) +
        # guard.box.w, wall.left.
        self.assertLessEqual(max(positions) + guard.box.w, wall.left)

    # МЕТОД EnemyTests.test_patrol_does_not_walk_off_unbounded_platform. Проверочный сценарий:
    # подготовка ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 129] Объявляем test_patrol_does_not_walk_off_unbounded_platform: тело ниже выполнится при вызове.
    # Отступы определяют, какие строки входят в метод.
    def test_patrol_does_not_walk_off_unbounded_platform(self):
        # [исх. 130] В floor записываем результат: создаём дробный прямоугольник с аргументами x, y, ширина,
        # высота; аргументы: 40, 100, 130, 10.
        floor = AABB(40, 100, 130, 10)
        # [исх. 131] В grid (сетка для быстрого поиска соседей или стен) записываем результат: строим индекс
        # неподвижных стен для быстрых локальных запросов; аргументы: [floor].
        grid = SpatialGrid([floor])
        # [исх. 132] В guard записываем результат: вызываем PatrolEnemy('test', AABB(90, 74, 18, 26), 0, 300);
        # параметры названы в определении этого метода.
        guard = PatrolEnemy("test", AABB(90, 74, 18, 26), 0, 300)
        # [исх. 133] Перебираем целые числа range(1600); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(1600):
            # [исх. 134] Вызываем guard.update(config.FIXED_DT, AABB(300, 200, 16, 26), grid); параметры названы в
            # определении этого метода.
            guard.update(config.FIXED_DT, AABB(300, 200, 16, 26), grid)
            # [исх. 135] Тест сравнивает дробные числа с допуском округления у self; аргументы: guard.box.bottom,
            # floor.top.
            self.assertAlmostEqual(guard.box.bottom, floor.top)
            # [исх. 136] Тест требует, чтобы первое число было не меньше второго у self; аргументы: guard.box.left,
            # floor.left - 1.
            self.assertGreaterEqual(guard.box.left, floor.left - 1)
            # [исх. 137] Тест требует, чтобы первое число было не больше второго у self; аргументы:
            # guard.box.right, floor.right + 1.
            self.assertLessEqual(guard.box.right, floor.right + 1)


# [исх. 140] Проверяем: __name__ равно '__main__'. При успехе выполняется вложенный блок.
if __name__ == "__main__":
    # [исх. 141] Вызываем unittest.main(); параметры названы в определении этого метода.
    unittest.main()
