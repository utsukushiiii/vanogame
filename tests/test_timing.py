# УЧЕБНАЯ ВЕРСИЯ byVanoGame — tests/test_timing.py
# Автоматическая проверка игры. Тесты создают ситуации, выполняют действия и сравнивают результат с
# ожидаемым.
# Комментарии [исх. N] ссылаются на строку N обычной версии проекта и руководства Word. В этой копии
# номера редактора больше из-за пояснений.
# Python игнорирует строки с #. Код и строковые значения сохранены; сборка отдельно сравнивает
# синтаксическое дерево и значимые токены.

# [исх. 1] Подключаем unittest: стандартный запуск тестов и проверки ожидаемых результатов.
import unittest

# [исх. 3] Импортируем FIXED_DT, MAX_STEPS из dormgame.config.
from dormgame.config import FIXED_DT, MAX_STEPS
# [исх. 4] Импортируем FixedStepper, InputBuffer из dormgame.timing.
from dormgame.timing import FixedStepper, InputBuffer


# [исх. 7] Объявляем класс TimingTests: описание будущих объектов. Наследуем возможности unittest.TestCase.
class TimingTests(unittest.TestCase):
    # МЕТОД TimingTests.test_edge_survives_frame_with_no_step. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 8] Объявляем test_edge_survives_frame_with_no_step: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_edge_survives_frame_with_no_step(self):
        # [исх. 9] В (inputs, clock) записываем результат: кортеж из 2 элементов, перечисленных ниже в коде.
        inputs, clock = InputBuffer(), FixedStepper()
        # [исх. 10] В commands (намерения игрока на один шаг) записываем результат: пустой список.
        commands = []
        # [исх. 11] Вызываем inputs.jump(True); параметры названы в определении этого метода.
        inputs.jump(True)
        # [исх. 12] Вызываем clock.advance(FIXED_DT / 3, lambda dt: commands.append(inputs.consume())); параметры
        # названы в определении этого метода.
        clock.advance(FIXED_DT / 3, lambda dt: commands.append(inputs.consume()))
        # [исх. 13] Тест требует равенства фактического и ожидаемого результата у self; аргументы: commands, [].
        self.assertEqual(commands, [])
        # [исх. 14] Вызываем clock.advance(3 * FIXED_DT, lambda dt: commands.append(inputs.consume())); параметры
        # названы в определении этого метода.
        clock.advance(3 * FIXED_DT, lambda dt: commands.append(inputs.consume()))
        # [исх. 15] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # sum((c.jump_pressed for c in commands)), 1.
        self.assertEqual(sum(c.jump_pressed for c in commands), 1)
        # [исх. 16] Тест требует истинного условия у self; аргументы: all((c.jump_held for c in commands)).
        self.assertTrue(all(c.jump_held for c in commands))

    # МЕТОД TimingTests.test_quick_press_release_preserved_in_order. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 18] Объявляем test_quick_press_release_preserved_in_order: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_quick_press_release_preserved_in_order(self):
        # [исх. 19] В inputs записываем результат: вызываем InputBuffer(); параметры названы в определении этого
        # метода.
        inputs = InputBuffer()
        # [исх. 20] Вызываем inputs.jump(True); параметры названы в определении этого метода.
        inputs.jump(True)
        # [исх. 21] Вызываем inputs.jump(False); параметры названы в определении этого метода.
        inputs.jump(False)
        # [исх. 22] Тест требует истинного условия у self; аргументы: inputs.consume().jump_pressed.
        self.assertTrue(inputs.consume().jump_pressed)
        # [исх. 23] Тест требует ложного условия у self; аргументы: inputs.consume().jump_held.
        self.assertFalse(inputs.consume().jump_held)
        # [исх. 24] Тест требует ложного условия у self; аргументы: inputs.consume().jump_pressed.
        self.assertFalse(inputs.consume().jump_pressed)

    # МЕТОД TimingTests.test_repeated_keydown_is_not_another_press. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 26] Объявляем test_repeated_keydown_is_not_another_press: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_repeated_keydown_is_not_another_press(self):
        # [исх. 27] В inputs записываем результат: вызываем InputBuffer(); параметры названы в определении этого
        # метода.
        inputs = InputBuffer()
        # [исх. 28] Перебираем целые числа range(10); правая граница не включается, третий аргумент задаёт шаг.
        # Очередной элемент записывается в _, затем выполняется вложенный блок.
        for _ in range(10):
            # [исх. 29] Вызываем inputs.jump(True); параметры названы в определении этого метода.
            inputs.jump(True)
        # [исх. 30] Тест требует истинного условия у self; аргументы: inputs.consume().jump_pressed.
        self.assertTrue(inputs.consume().jump_pressed)
        # [исх. 31] Тест требует ложного условия у self; аргументы: inputs.consume().jump_pressed.
        self.assertFalse(inputs.consume().jump_pressed)

    # МЕТОД TimingTests.test_two_distinct_presses_both_consumed. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 33] Объявляем test_two_distinct_presses_both_consumed: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_two_distinct_presses_both_consumed(self):
        # [исх. 34] В inputs записываем результат: вызываем InputBuffer(); параметры названы в определении этого
        # метода.
        inputs = InputBuffer()
        # [исх. 35] Перебираем кортеж из 4 элементов, перечисленных ниже в коде. Очередной элемент записывается в
        # state, затем выполняется вложенный блок.
        for state in (True, False, True, False):
            # [исх. 36] Вызываем inputs.jump(state); параметры названы в определении этого метода.
            inputs.jump(state)
        # [исх. 37] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # sum((inputs.consume().jump_pressed for _ in range(8))), 2.
        self.assertEqual(sum(inputs.consume().jump_pressed for _ in range(8)), 2)

    # МЕТОД TimingTests.test_interact_reset_are_one_shot. Проверочный сценарий: подготовка ситуации,
    # действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 39] Объявляем test_interact_reset_are_one_shot: тело ниже выполнится при вызове. Отступы определяют,
    # какие строки входят в метод.
    def test_interact_reset_are_one_shot(self):
        # [исх. 40] В inputs записываем результат: вызываем InputBuffer(); параметры названы в определении этого
        # метода.
        inputs = InputBuffer()
        # [исх. 41] Вызываем inputs.interact(); параметры названы в определении этого метода.
        inputs.interact()
        # [исх. 42] Вызываем inputs.reset_checkpoint(); параметры названы в определении этого метода.
        inputs.reset_checkpoint()
        # [исх. 43] В (first, second) записываем результат: кортеж из 2 элементов, перечисленных ниже в коде.
        first, second = inputs.consume(), inputs.consume()
        # [исх. 44] Тест требует истинного условия у self; аргументы: first.interact and first.reset.
        self.assertTrue(first.interact and first.reset)
        # [исх. 45] Тест требует ложного условия у self; аргументы: second.interact or second.reset.
        self.assertFalse(second.interact or second.reset)

    # МЕТОД TimingTests.test_catch_up_is_limited. Проверочный сценарий: подготовка ситуации, действие,
    # сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 47] Объявляем test_catch_up_is_limited: тело ниже выполнится при вызове. Отступы определяют, какие
    # строки входят в метод.
    def test_catch_up_is_limited(self):
        # [исх. 48] В (clock, ticks) записываем результат: кортеж из 2 элементов, перечисленных ниже в коде.
        clock, ticks = FixedStepper(), []
        # [исх. 49] Вызываем clock.advance(30.0, lambda dt: ticks.append(dt)); параметры названы в определении
        # этого метода.
        clock.advance(30.0, lambda dt: ticks.append(dt))
        # [исх. 50] Тест требует, чтобы первое число было не больше второго у self; аргументы: len(ticks),
        # MAX_STEPS.
        self.assertLessEqual(len(ticks), MAX_STEPS)
        # [исх. 51] Тест требует, чтобы первое число было не больше второго у self; аргументы: sum(ticks), 0.101.
        self.assertLessEqual(sum(ticks), 0.101)

    # МЕТОД TimingTests.test_pause_drops_accumulator_without_advancing. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 53] Объявляем test_pause_drops_accumulator_without_advancing: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_pause_drops_accumulator_without_advancing(self):
        # [исх. 54] В (clock, ticks) записываем результат: кортеж из 2 элементов, перечисленных ниже в коде.
        clock, ticks = FixedStepper(), []
        # [исх. 55] Вызываем clock.advance(FIXED_DT / 2, lambda dt: ticks.append(dt)); параметры названы в
        # определении этого метода.
        clock.advance(FIXED_DT / 2, lambda dt: ticks.append(dt))
        # [исх. 56] Вызываем clock.advance(30, lambda dt: ticks.append(dt)); параметры названы в определении этого
        # метода.
        clock.advance(30, lambda dt: ticks.append(dt), paused=True)
        # [исх. 57] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # clock.accumulator, 0.0.
        self.assertEqual(clock.accumulator, 0.0)
        # [исх. 58] Тест требует равенства фактического и ожидаемого результата у self; аргументы: ticks, [].
        self.assertEqual(ticks, [])
        # [исх. 59] Вызываем clock.advance(FIXED_DT, lambda dt: ticks.append(dt)); параметры названы в определении
        # этого метода.
        clock.advance(FIXED_DT, lambda dt: ticks.append(dt))
        # [исх. 60] Тест требует равенства фактического и ожидаемого результата у self; аргументы: ticks,
        # [FIXED_DT].
        self.assertEqual(ticks, [FIXED_DT])

    # МЕТОД TimingTests.test_stop_transition_cancels_remaining_steps. Проверочный сценарий: подготовка
    # ситуации, действие, сравнение с ожидаемым результатом.
    # Параметр self: текущий объект.
    # [исх. 62] Объявляем test_stop_transition_cancels_remaining_steps: тело ниже выполнится при вызове. Отступы
    # определяют, какие строки входят в метод.
    def test_stop_transition_cancels_remaining_steps(self):
        # [исх. 63] В clock записываем результат: вызываем FixedStepper(); параметры названы в определении этого
        # метода.
        clock = FixedStepper()
        # [исх. 64] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # clock.advance(0.1, lambda dt: False), 1.
        self.assertEqual(clock.advance(0.1, lambda dt: False), 1)
        # [исх. 65] Тест требует равенства фактического и ожидаемого результата у self; аргументы:
        # clock.accumulator, 0.0.
        self.assertEqual(clock.accumulator, 0.0)


# [исх. 68] Проверяем: __name__ равно '__main__'. При успехе выполняется вложенный блок.
if __name__ == '__main__':
    # [исх. 69] Вызываем unittest.main(); параметры названы в определении этого метода.
    unittest.main()
