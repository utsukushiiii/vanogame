# УЧЕБНАЯ ВЕРСИЯ byVanoGame — tools/verify_pygame.py
# Автоматическая проверка игры. Тесты создают ситуации, выполняют действия и сравнивают результат с
# ожидаемым.
# Комментарии [исх. N] ссылаются на строку N обычной версии проекта и руководства Word. В этой копии
# номера редактора больше из-за пояснений.
# Python игнорирует строки с #. Код и строковые значения сохранены; сборка отдельно сравнивает
# синтаксическое дерево и значимые токены.

# [исх. 1] Строка документации объясняет назначение модуля, класса или функции; игровые действия здесь не
# выполняются.
"""Проверка настоящего Pygame-приложения и снимки экранов.

python -m tools.verify_pygame             dummy SDL
python -m tools.verify_pygame --native    настоящее окно Windows

Контроллер посылает события кнопок и использует тот же фиксированный шаг.
Это автоматизированный прогон, а не ручное прохождение человеком.
"""
# [исх. 9] Подключаем annotations: annotations откладывает вычисление аннотаций типов: можно ссылаться на класс
# до окончания его объявления.
from __future__ import annotations

# [исх. 11] Подключаем argparse: разбор флагов запуска вроде --level 2 или --debug.
import argparse
# [исх. 12] Подключаем json: преобразование JSON-текста в словари/списки и обратно.
import json
# [исх. 13] Подключаем os: настройки окружения процесса, в том числе драйверы SDL для проверки без окна.
import os
# [исх. 14] Подключаем Path: Path строит пути к файлам и читает/записывает их без ручного склеивания разделителей.
from pathlib import Path
# [исх. 15] Подключаем TemporaryDirectory: временные файлы и папки, изолирующие проверки настроек.
from tempfile import TemporaryDirectory


# МЕТОД verify. Вспомогательная функция проверки; действия подробно разобраны ниже.
# Параметр native: входное значение; использование показано в строках тела; ожидаемый тип bool; если не
# передать, используется False.
# После -> указан ожидаемый тип результата: dict. Это подсказка, не автоматическая проверка.
# [исх. 18] Объявляем verify: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в метод.
def verify(native: bool = False) -> dict:
    # [исх. 19] Берём существующее значение по ключу либо создаём начальное у os.environ; аргументы:
    # 'PYGAME_HIDE_SUPPORT_PROMPT', '1'.
    os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
    # [исх. 20] Проверяем: native ложно, равно нулю или пусто. При успехе выполняется вложенный блок.
    if not native:
        # [исх. 21] Берём существующее значение по ключу либо создаём начальное у os.environ; аргументы:
        # 'SDL_VIDEODRIVER', 'dummy'.
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        # [исх. 22] Берём существующее значение по ключу либо создаём начальное у os.environ; аргументы:
        # 'SDL_AUDIODRIVER', 'dummy'.
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
    # [исх. 23] Подключаем pygame: окно, клавиатура, рисование и звук; импорт сам по себе ещё не открывает окно.
    import pygame
    # [исх. 24] Импортируем Application, Settings из dormgame.app.
    from dormgame.app import Application, Settings
    # [исх. 25] Импортируем FIXED_DT из dormgame.config.
    from dormgame.config import FIXED_DT
    # [исх. 26] Импортируем RouteController, route_one, route_two, route_three из tools.verify_routes.
    from tools.verify_routes import RouteController, route_one, route_two, route_three

    # [исх. 28] В output записываем результат: деление в формуле Path(__file__).resolve().parents[1] /
    # 'artifacts'.
    output = Path(__file__).resolve().parents[1] / 'artifacts'
    # [исх. 29] Создаём каталог; parents разрешает вложенные, exist_ok допускает уже существующий у output.
    output.mkdir(exist_ok=True)
    # [исх. 30] В app записываем результат: вызываем Application(); параметры названы в определении этого метода.
    app = Application(smoke=True)
    # [исх. 31] В snapshots записываем результат: пустой список.
    snapshots: list[str] = []

    # МЕТОД verify.key. Вспомогательная функция проверки; действия подробно разобраны ниже.
    # Параметр code: входное значение; использование показано в строках тела; ожидаемый тип int.
    # Параметр pressed: новое состояние кнопки: нажато или отпущено; ожидаемый тип bool; если не
    # передать, используется True.
    # После -> указан ожидаемый тип результата: None. Это подсказка, не автоматическая проверка.
    # [исх. 33] Объявляем key: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в метод.
    def key(code: int, pressed: bool = True) -> None:
        # [исх. 34] Вызываем app.handle_event(pygame.event.Event(pygame.KEYDOWN if pressed else pygame.KEYUP,
        # key=code, repeat=False)); параметры названы в определении этого метода.
        app.handle_event(pygame.event.Event(pygame.KEYDOWN if pressed else pygame.KEYUP,
                                           # [исх. 35] Продолжение выражения выше: code.
                                           key=code, repeat=False))

    # МЕТОД verify.capture. Вспомогательная функция проверки; действия подробно разобраны ниже.
    # Параметр name: имя настройки, звука или другого выбираемого элемента; ожидаемый тип str.
    # После -> указан ожидаемый тип результата: None. Это подсказка, не автоматическая проверка.
    # [исх. 37] Объявляем capture: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в
    # метод.
    def capture(name: str) -> None:
        # [исх. 38] Вызываем app.render(0); параметры названы в определении этого метода.
        app.render(0)
        # [исх. 39] Сохраняем отрисованный холст в PNG для проверки; аргументы: app.window, str(output /
        # f'{name}.png').
        pygame.image.save(app.window, str(output / f'{name}.png'))
        # [исх. 40] Добавляем один элемент в конец у snapshots; аргументы: name.
        snapshots.append(name)

    # [исх. 42] Объявляем класс WindowController: описание будущих объектов. Наследуем возможности
    # RouteController.
    class WindowController(RouteController):
        # МЕТОД verify.WindowController.tick. Вспомогательная функция проверки; действия подробно
        # разобраны ниже.
        # Параметр self: текущий объект.
        # Параметр move: направление бега: -1, 0 или 1; если не передать, используется 0.
        # Параметр jump: входное значение; использование показано в строках тела; если не передать,
        # используется False.
        # Параметр held: входное значение; использование показано в строках тела; если не передать,
        # используется False.
        # Параметр interact: разовый запрос действия E; если не передать, используется False.
        # [исх. 43] Объявляем tick: тело ниже выполнится при вызове. Отступы определяют, какие строки входят в
        # метод.
        def tick(self, move=0, jump=False, held=False, interact=False):
            # [исх. 44] В deaths (число смертей и возвратов по R) записываем результат: app.session.deaths (число
            # смертей и возвратов по R).
            deaths = app.session.deaths
            # [исх. 45] В app.input.move (направление бега: -1, 0 или 1) записываем результат: move (направление
            # бега: -1, 0 или 1).
            app.input.move = move
            # [исх. 46] Проверяем: jump имеет истинное значение (не False, не None, не ноль и не пустая
            # коллекция). При успехе выполняется вложенный блок.
            if jump:
                # [исх. 47] Вызываем key(pygame.K_SPACE); параметры названы в определении этого метода.
                key(pygame.K_SPACE)
            # [исх. 48] Проверяем: held ложно, равно нулю или пусто; одновременно app.input.held имеет истинное
            # значение (не False, не None, не ноль и не пустая коллекция). При успехе выполняется
            # вложенный блок.
            if not held and app.input.held:
                # [исх. 49] Вызываем key(pygame.K_SPACE, False); параметры названы в определении этого метода.
                key(pygame.K_SPACE, False)
            # [исх. 50] Проверяем: interact имеет истинное значение (не False, не None, не ноль и не пустая
            # коллекция). При успехе выполняется вложенный блок.
            if interact:
                # [исх. 51] Вызываем key(pygame.K_e); параметры названы в определении этого метода.
                key(pygame.K_e)
            # [исх. 52] Вызываем app.stepper.advance(FIXED_DT, app.step); параметры названы в определении этого
            # метода.
            app.stepper.advance(FIXED_DT, app.step, paused=app.scene != 'game')
            # [исх. 53] В events (накопленные сообщения о произошедшем) записываем результат: вызываем
            # app.session.drain_events(); параметры названы в определении этого метода.
            events = app.session.drain_events()
            # [исх. 54] Меняем self.jumps: прибавляем суммируем значения; True считается 1, False — 0; аргументы:
            # (e.kind == 'jump' for e in events) и сохраняем обратно.
            self.jumps += sum(e.kind == 'jump' for e in events)
            # [исх. 55] Меняем self.steps (число выполненных физических шагов): прибавляем число 1 и сохраняем
            # обратно.
            self.steps += 1
            # [исх. 56] Вызываем app.renderer.accept_events(events, app.settings); параметры названы в определении
            # этого метода.
            app.renderer.accept_events(events, app.settings)
            # [исх. 57] Перебираем events (накопленные сообщения о произошедшем). Очередной элемент записывается в
            # event, затем выполняется вложенный блок.
            for event in events:
                # [исх. 58] Запускаем воспроизведение звука у app.audio; аргументы: event.kind.
                app.audio.play(event.kind)
            # [исх. 59] Вызываем app.renderer.tick(FIXED_DT, app.settings); параметры названы в определении этого
            # метода.
            app.renderer.tick(FIXED_DT, app.settings)
            # [исх. 60] Проверяем: self.steps % 4 равно 0. При успехе выполняется вложенный блок.
            if self.steps % 4 == 0:
                # [исх. 61] Вызываем app.render(4 * FIXED_DT); параметры названы в определении этого метода.
                app.render(4 * FIXED_DT)
                # [исх. 62] Вызываем pygame.event.pump(); параметры названы в определении этого метода.
                pygame.event.pump()
            # [исх. 63] В around_wall записываем результат: проверяем, истинно ли хотя бы одно из условий;
            # аргументы: (enemy.kind == 'drone' and enemy.state == 'Погоня' and any((648 <=
            # enemy.nav.cell_center(cell)[0] <= 680 and enemy.nav.cell_center(cell)[1] >= 376 for cell
            # in enemy.path)) for enemy in app.session.level.enemies).
            around_wall = any(
                # [исх. 64] Продолжение выражения выше: enemy.kind равно 'drone'; одновременно enemy.state равно
                # 'Погоня'; одновременно any((648 <= enemy.nav.cell_center(cell)[0] <= 680 and
                # enemy.nav.cell_center(cell)[1] >= 376 for cell in enemy.path)) имеет истинное значение
                # (не False, не None, не ноль и не пустая коллекция).
                enemy.kind == 'drone' and enemy.state == 'Погоня'
                # [исх. 65] Продолжение выражения выше: проверяем, истинно ли хотя бы одно из условий; аргументы:
                # (648 <= enemy.nav.cell_center(cell)[0] <= 680 and enemy.nav.cell_center(cell)[1] >=
                # 376 for cell in enemy.path).
                and any(648 <= enemy.nav.cell_center(cell)[0] <= 680
                        # [исх. 66] Продолжение выражения выше: enemy.nav.cell_center(cell)[1] не меньше 376.
                        and enemy.nav.cell_center(cell)[1] >= 376 for cell in enemy.path)
                # [исх. 67] Продолжение выражения выше: enemy.
                for enemy in app.session.level.enemies)
            # [исх. 68] Проверяем: app.session.level_index равно 1; одновременно around_wall имеет истинное
            # значение (не False, не None, не ноль и не пустая коллекция); одновременно 'astar-wall'
            # отсутствует в snapshots. При успехе выполняется вложенный блок.
            if app.session.level_index == 1 and around_wall and 'astar-wall' not in snapshots:
                # [исх. 69] В app.debug (включена ли схема F3) записываем результат: True — да, условие выполнено.
                app.debug = True
                # [исх. 70] Вызываем capture('astar-wall'); параметры названы в определении этого метода.
                capture('astar-wall')
                # [исх. 71] В app.debug (включена ли схема F3) записываем результат: False — нет, условие не
                # выполнено.
                app.debug = False
            # [исх. 72] Проверяем обязательное условие app.session.deaths равно deaths; при нарушении assert
            # сообщает об ошибке проверки.
            assert app.session.deaths == deaths, f'Смерть при проверке экрана {app.scene}'

    # [исх. 74] Пробуем выполнить вложенные действия; перечисленные ниже except перехватят ожидаемые ошибки.
    try:
        # [исх. 75] Вызываем capture('menu'); параметры названы в определении этого метода.
        capture('menu')
        # Навигация кнопками, мышь после изменения пропорций окна.
        # [исх. 77] Вызываем key(pygame.K_DOWN); параметры названы в определении этого метода.
        key(pygame.K_DOWN)
        # [исх. 78] Вызываем key(pygame.K_RETURN); параметры названы в определении этого метода.
        key(pygame.K_RETURN)
        # [исх. 79] Проверяем обязательное условие app.scene равно 'controls'; при нарушении assert сообщает об
        # ошибке проверки.
        assert app.scene == 'controls'
        # [исх. 80] Вызываем capture('controls'); параметры названы в определении этого метода.
        capture('controls')
        # [исх. 81] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 82] Вызываем app.activate(2); параметры названы в определении этого метода.
        app.activate(2)
        # [исх. 83] Вызываем capture('settings'); параметры названы в определении этого метода.
        capture('settings')
        # [исх. 84] Вызываем app.activate(2); параметры названы в определении этого метода.
        app.activate(2)
        # [исх. 85] Вызываем app.activate(3); параметры названы в определении этого метода.
        app.activate(3)
        # [исх. 86] Проверяем обязательное условие app.settings.shake ложно, равно нулю или пусто; одновременно
        # app.settings.reduced_effects имеет истинное значение (не False, не None, не ноль и не пустая
        # коллекция); при нарушении assert сообщает об ошибке проверки.
        assert not app.settings.shake and app.settings.reduced_effects
        # [исх. 87] Вызываем app.activate(2); параметры названы в определении этого метода.
        app.activate(2)
        # [исх. 88] Вызываем app.activate(3); параметры названы в определении этого метода.
        app.activate(3)
        # [исх. 89] Открываем управляемый блок: менеджер контекста освобождает ресурс или проверяет ожидаемое
        # исключение после выхода.
        with TemporaryDirectory() as directory:
            # [исх. 90] В path (путь к файлу или последовательность клеток — зависит от метода) записываем
            # результат: деление в формуле Path(directory) / 'settings.json'.
            path = Path(directory) / 'settings.json'
            # [исх. 91] Вызываем app.settings.save(path); параметры названы в определении этого метода.
            app.settings.save(path)
            # [исх. 92] Проверяем обязательное условие Settings.load(path) равно app.settings; при нарушении
            # assert сообщает об ошибке проверки.
            assert Settings.load(path) == app.settings
        # [исх. 93] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 94] В app.window (окно Pygame или нарисованное декоративное окно — зависит от метода) записываем
        # результат: создаём или перенастраиваем экранную поверхность; аргументы: (1000, 700),
        # pygame.RESIZABLE.
        app.window = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
        # [исх. 95] Вызываем app.render(0); параметры названы в определении этого метода.
        app.render(0)
        # [исх. 96] Проверяем обязательное условие app.viewport.height меньше 700; одновременно app.viewport.width
        # равно 1000; при нарушении assert сообщает об ошибке проверки.
        assert app.viewport.height < 700 and app.viewport.width == 1000
        # [исх. 97] В button записываем результат: элемент app.buttons по индексу или ключу 0.
        button = app.buttons[0]
        # [исх. 98] В mouse записываем результат: кортеж из 2 элементов, перечисленных ниже в коде.
        mouse = (round(app.viewport.x + button.centerx * app.viewport.w / 640),
                 # [исх. 99] Продолжение выражения выше: округляем число; аргументы: app.viewport.y +
                 # button.centery * app.viewport.h / 360.
                 round(app.viewport.y + button.centery * app.viewport.h / 360))
        # [исх. 100] Вызываем app.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=mouse));
        # параметры названы в определении этого метода.
        app.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=mouse))
        # [исх. 101] Проверяем обязательное условие app.scene равно 'intro'; при нарушении assert сообщает об
        # ошибке проверки.
        assert app.scene == 'intro'
        # [исх. 102] Вызываем capture('intro-letterbox'); параметры названы в определении этого метода.
        capture('intro-letterbox')
        # [исх. 103] В app.window (окно Pygame или нарисованное декоративное окно — зависит от метода) записываем
        # результат: создаём или перенастраиваем экранную поверхность; аргументы: (1280, 720),
        # pygame.RESIZABLE.
        app.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        # [исх. 104] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 105] Проверяем обязательное условие app.scene равно 'game'; при нарушении assert сообщает об ошибке
        # проверки.
        assert app.scene == 'game'
        # [исх. 106] Вызываем key(pygame.K_SPACE); параметры названы в определении этого метода.
        key(pygame.K_SPACE)
        # [исх. 107] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 108] В before записываем результат: app.session.elapsed (игровое время в секундах).
        before = app.session.elapsed
        # [исх. 109] Вызываем app.update(10); параметры названы в определении этого метода.
        app.update(10)
        # [исх. 110] Проверяем обязательное условие app.session.elapsed равно before; одновременно
        # app.stepper.accumulator равно 0; при нарушении assert сообщает об ошибке проверки.
        assert app.session.elapsed == before and app.stepper.accumulator == 0
        # [исх. 111] Вызываем capture('pause'); параметры названы в определении этого метода.
        capture('pause')
        # [исх. 112] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 113] Проверяем обязательное условие app.input.consume().jump_pressed ложно, равно нулю или пусто;
        # при нарушении assert сообщает об ошибке проверки.
        assert not app.input.consume().jump_pressed
        # [исх. 114] Вызываем app.handle_event(pygame.event.Event(pygame.WINDOWFOCUSLOST)); параметры названы в
        # определении этого метода.
        app.handle_event(pygame.event.Event(pygame.WINDOWFOCUSLOST))
        # [исх. 115] Проверяем обязательное условие app.scene равно 'pause'; при нарушении assert сообщает об
        # ошибке проверки.
        assert app.scene == 'pause'
        # [исх. 116] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 117] Вызываем key(pygame.K_m); параметры названы в определении этого метода.
        key(pygame.K_m)
        # [исх. 118] Проверяем обязательное условие app.settings.sound ложно, равно нулю или пусто; при нарушении
        # assert сообщает об ошибке проверки.
        assert not app.settings.sound
        # [исх. 119] Вызываем key(pygame.K_m); параметры названы в определении этого метода.
        key(pygame.K_m)
        # [исх. 120] Проверяем обязательное условие app.settings.sound имеет истинное значение (не False, не None,
        # не ноль и не пустая коллекция); при нарушении assert сообщает об ошибке проверки.
        assert app.settings.sound
        # [исх. 121] Вызываем key(pygame.K_F3); параметры названы в определении этого метода.
        key(pygame.K_F3)
        # [исх. 122] Проверяем обязательное условие app.debug имеет истинное значение (не False, не None, не ноль и
        # не пустая коллекция); при нарушении assert сообщает об ошибке проверки.
        assert app.debug
        # [исх. 123] Вызываем key(pygame.K_F3); параметры названы в определении этого метода.
        key(pygame.K_F3)
        # [исх. 124] В controller записываем результат: вызываем WindowController(app.session); параметры названы в
        # определении этого метода.
        controller = WindowController(app.session)
        # [исх. 125] Перебираем получаем одновременно индекс с нуля и сам элемент; аргументы: (route_one,
        # route_two, route_three). Очередной элемент записывается в (index, route), затем выполняется
        # вложенный блок.
        for index, route in enumerate((route_one, route_two, route_three)):
            # [исх. 126] Вызываем capture(f'level{index + 1}-start'); параметры названы в определении этого метода.
            capture(f'level{index + 1}-start')
            # [исх. 127] Вызываем controller.walk(8); параметры названы в определении этого метода.
            controller.walk(8)
            # [исх. 128] Вызываем controller.walk(48); параметры названы в определении этого метода.
            controller.walk(48)
            # [исх. 129] Вызываем capture(f'souvenir{index + 1}'); параметры названы в определении этого метода.
            capture(f'souvenir{index + 1}')
            # [исх. 130] Вызываем route(controller); параметры названы в определении этого метода.
            route(controller)
            # [исх. 131] Проверяем обязательное условие app.session.level.complete имеет истинное значение (не
            # False, не None, не ноль и не пустая коллекция); при нарушении assert сообщает об ошибке
            # проверки.
            assert app.session.level.complete
            # [исх. 132] Проверяем: index меньше 2. При успехе выполняется вложенный блок.
            if index < 2:
                # [исх. 133] Проверяем обязательное условие app.scene равно 'transition'; при нарушении assert
                # сообщает об ошибке проверки.
                assert app.scene == 'transition'
                # [исх. 134] Вызываем capture(f'transition{index + 1}'); параметры названы в определении этого
                # метода.
                capture(f'transition{index + 1}')
                # [исх. 135] Вызываем key(pygame.K_RETURN); параметры названы в определении этого метода.
                key(pygame.K_RETURN)
                # [исх. 136] Проверяем обязательное условие app.scene равно 'game'; одновременно
                # app.session.level_index равно index + 1; при нарушении assert сообщает об ошибке
                # проверки.
                assert app.scene == 'game' and app.session.level_index == index + 1
            # [исх. 137] Альтернативная ветка: предыдущие условия не подошли, поэтому выполняется этот блок.
            else:
                # [исх. 138] Проверяем обязательное условие app.scene равно 'ending'; одновременно
                # app.session.finished имеет истинное значение (не False, не None, не ноль и не пустая
                # коллекция); при нарушении assert сообщает об ошибке проверки.
                assert app.scene == 'ending' and app.session.finished
        # [исх. 139] Проверяем обязательное условие app.session.total_pages равно 13; одновременно
        # app.session.deaths равно 0; при нарушении assert сообщает об ошибке проверки.
        assert app.session.total_pages == 13 and app.session.deaths == 0
        # [исх. 140] Проверяем обязательное условие app.session.total_souvenirs равно 3; при нарушении assert
        # сообщает об ошибке проверки.
        assert app.session.total_souvenirs == 3
        # [исх. 141] Вызываем capture('ending'); параметры названы в определении этого метода.
        capture('ending')
        # [исх. 142] В result записываем результат: словарь из 9 элементов, перечисленных ниже в коде.
        result = {'video_driver': pygame.display.get_driver(), 'audio': app.audio.available,
                  # [исх. 143] Продолжение выражения выше: текст 'completed'.
                  'completed': app.session.finished, 'pages': app.session.total_pages,
                  # [исх. 144] Продолжение выражения выше: текст 'deaths'.
                  'deaths': app.session.deaths, 'seconds': round(app.session.elapsed, 3),
                  # [исх. 145] Продолжение выражения выше: текст 'souvenirs'.
                  'souvenirs': app.session.total_souvenirs,
                  # [исх. 146] Продолжение выражения выше: текст 'jumps'.
                  'jumps': controller.jumps, 'snapshots': snapshots}
        # [исх. 147] Вызываем key(pygame.K_RETURN); параметры названы в определении этого метода.
        key(pygame.K_RETURN)
        # [исх. 148] Проверяем обязательное условие app.scene равно 'intro'; одновременно app.session.total_pages
        # равно 0; одновременно app.session.elapsed равно 0; при нарушении assert сообщает об ошибке
        # проверки.
        assert app.scene == 'intro' and app.session.total_pages == 0 and app.session.elapsed == 0
        # [исх. 149] Вызываем key(pygame.K_ESCAPE); параметры названы в определении этого метода.
        key(pygame.K_ESCAPE)
        # [исх. 150] Проверяем обязательное условие app.scene равно 'game'; при нарушении assert сообщает об ошибке
        # проверки.
        assert app.scene == 'game'
        # [исх. 151] В result['restart_verified'] записываем результат: True — да, условие выполнено.
        result['restart_verified'] = True
        # [исх. 152] Записываем текст в файл у output / ('native-check.json' if native else 'pygame-check.json');
        # аргументы: json.dumps(result, ensure_ascii=False, indent=2).
        (output / ('native-check.json' if native else 'pygame-check.json')).write_text(
            # [исх. 153] Продолжение выражения выше: превращаем данные Python в JSON-текст; аргументы: result.
            json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        # [исх. 154] Завершаем этот вызов и возвращаем вызывающему коду: result.
        return result
    # [исх. 155] Блок выполняется при любом выходе из try, включая исключение; здесь освобождаются ресурсы.
    finally:
        # [исх. 156] Вызываем app.close(); параметры названы в определении этого метода.
        app.close()


# [исх. 159] Проверяем: __name__ равно '__main__'. При успехе выполняется вложенный блок.
if __name__ == '__main__':
    # [исх. 160] В parser (разборщик аргументов запуска) записываем результат: вызываем argparse.ArgumentParser();
    # параметры названы в определении этого метода.
    parser = argparse.ArgumentParser(description=__doc__)
    # [исх. 161] Вызываем parser.add_argument('--native'); параметры названы в определении этого метода.
    parser.add_argument('--native', action='store_true')
    # [исх. 162] В arguments записываем результат: вызываем parser.parse_args(); параметры названы в определении
    # этого метода.
    arguments = parser.parse_args()
    # [исх. 163] Выводим результат в консоль; аргументы: json.dumps(verify(arguments.native), ensure_ascii=False,
    # indent=2).
    print(json.dumps(verify(arguments.native), ensure_ascii=False, indent=2))
