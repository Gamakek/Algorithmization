import pygame  
from queue import PriorityQueue 

pygame.init()

WIDTH = 600  # Ширина и высота окна приложения в пикселях
GRID_SIZE = 10  # Размер квадратной сетки лабиринта
CELL_SIZE = WIDTH // GRID_SIZE  # Расчет размера одной ячейки в пикселях (600 / 10 = 60 пикселей)

# Создаем окно
WIN = pygame.display.set_mode((WIDTH, WIDTH))

RED = (255, 0, 0)          # Красный: посещенные ячейки
GREEN = (0, 255, 0)        # Зеленый: ячейки, находящиеся на рассмотрении
WHITE = (255, 255, 255)    # Белый: пустая ячейка
BLACK = (0, 0, 0)          # Черный: препятствие
PURPLE = (128, 0, 128)      # Фиолетовый: итоговый путь
ORANGE = (255, 165, 0)      # Оранжевый: стартовая ячейка
TURQUOISE = (64, 224, 208)  # Бирюзовый: целевая ячейка
GREY = (128, 128, 128)      # Серый: сетка


class Cell:
    """Класс, описывающий отдельную ячейку на игровом поле."""

    def __init__(self, row, col):
        self.row = row  # Индекс строки
        self.col = col  # Индекс столбца
        self.x = col * CELL_SIZE  # Координата X 
        self.y = row * CELL_SIZE  # Координата Y
        self.color = WHITE  # Начальный цвет ячейки
        self.neighbors = []  # Список соседних ячеек

    def get_pos(self):
        """Возвращает позицию ячейки в формате кортежа (строка, столбец)."""
        return self.row, self.col

    def is_closed(self):
        """Проверяет, помечена ли ячейка как закрытая (красная)."""
        return self.color == RED

    def is_open(self):
        """Проверяет, находится ли ячейка в открытом списке (зеленая)."""
        return self.color == GREEN

    def is_barrier(self):
        """Проверяет, является ли ячейка стеной (черная)."""
        return self.color == BLACK

    def is_start(self):
        """Проверяет, является ли ячейка стартовой (оранжевая)."""
        return self.color == ORANGE

    def is_end(self):
        """Проверяет, является ли ячейка целевой (бирюзовая)."""
        return self.color == TURQUOISE

    def reset(self):
        """Сбрасывает состояние ячейки к значению по умолчанию (белая)."""
        self.color = WHITE

    def make_start(self):
        """Устанавливает статус стартовой ячейки."""
        self.color = ORANGE

    def make_closed(self):
        """Помечает ячейку как исследованную (закрытую)."""
        self.color = RED

    def make_open(self):
        """Добавляет ячейку в список кандидатов на рассмотрение (открытую)."""
        self.color = GREEN

    def make_barrier(self):
        """Устанавливает ячейку в качестве непроходимой стены."""
        self.color = BLACK

    def make_end(self):
        """Устанавливает статус целевой ячейки."""
        self.color = TURQUOISE

    def make_path(self):
        """Окрашивает ячейку в цвет итогового пути."""
        self.color = PURPLE

    def draw(self, win):
        """Отрисовывает квадратную ячейку."""
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        """Анализирует 4 соседних направления и добавляет свободные ячейки в список neighbors."""
        self.neighbors = []  # Очищаем старый список соседей

        # Проверка соседа снизу (если строка не последняя и сосед снизу — не препятствие)
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Проверка соседа сверху (если строка не первая и сосед сверху — не препятствие)
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Проверка соседа справа (если столбец не крайний правый и сосед справа — не препятствие)
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Проверка соседа слева (если столбец не крайний левый и сосед слева — не препятствие)
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def heuristic(p1, p2):
    """Вычисляет Манхэттенское расстояние между двумя точками."""
    r1, c1 = p1  # Координаты первой точки
    r2, c2 = p2  # Координаты второй точки
    return abs(r1 - r2) + abs(c1 - c2)


def reconstruct_path(came_from, current, draw):
    """Восстанавливает и визуализирует путь в обратном порядке от финиша к старту."""
    while current in came_from:  # Пока для текущей ячейки существует родительская запись
        current = came_from[current]  # Переходим к родительской ячейке
        if not current.is_start():  # Если ячейка не является стартовой
            current.make_path()  # Окрашиваем ее в фиолетовый цвет пути
        draw()  # Обновляем кадр


def a_star_algorithm(draw, grid, start, end):
    """Реализация алгоритма поиска пути A*."""
    count = 0  # Счётчик для отслеживания порядка добавления элементов с одинаковым f_score
    open_set = PriorityQueue()  # Создаем приоритетную очередь
    # Добавляем стартовую вершину в очередь: кортеж (f_score, порядковый_номер, объект_ячейки)
    open_set.put((0, count, start))
    came_from = {}  # Словарь для хранения связей «дочерняя ячейка: родительская ячейка»

    # Инициализация g_score (расстояние от старта) бесконечностью для всех ячеек
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0  # Стоимость пути от старта до самого себя равна 0

    # Инициализация f_score (g + эвристика h) бесконечностью для всех ячеек
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    # Вспомогательное множество для быстрой проверки наличия ячейки в приоритетной очереди
    open_set_hash = {start}

    # Пока в открытом списке есть элементы для исследования
    while not open_set.empty():
        # Обрабатываем события Pygame, чтобы окно не зависало во время поиска
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Извлекаем ячейку с наименьшим значением f_score
        current = open_set.get()[2]
        open_set_hash.remove(current)  # Синхронно удаляем ее из множества

        # Если мы достигли целевой ячейки — путь успешно найден
        if current == end:
            reconstruct_path(came_from, end, draw)  # Восстанавливаем весь путь
            end.make_end()  # Принудительно сохраняем цвет финиша
            return True

        # Исследуем всех соседей текущей ячейки
        for neighbor in current.neighbors:
            # Вычисляем временную стоимость g_score для соседа (стоимость шага = 1)
            temp_g_score = g_score[current] + 1

            # Если новый найденный путь к соседу короче, чем ранее сохраненный
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current  # Запоминаем, откуда пришли в соседа
                g_score[neighbor] = temp_g_score  # Обновляем стоимость пути от старта
                # Рассчитываем полную стоимость f_score для соседа
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())

                # Если сосед еще не был добавлен в открытый список на исследование
                if neighbor not in open_set_hash:
                    count += 1  # Увеличиваем счетчик порядка добавления
                    # Добавляем соседа в приоритетную очередь
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)  # Синхронизируем со множеством
                    if not neighbor.is_end():  # Если сосед не финиш
                        neighbor.make_open()  # Помечаем его зеленым цветом (в очереди)

        draw()  # Перерисовываем экран для отображения изменений на текущем шаге

        # Если рассмотренная ячейка не является стартом, закрываем её (окрашиваем в красный)
        if current != start:
            current.make_closed()

    return False  # Возвращаем False, если вся сетка проверена, а путь к финишу не существует


def make_grid():
    """Создает двумерную матрицу объектов Cell размера GRID_SIZE на GRID_SIZE."""
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])  # Добавляем новую пустую строку
        for j in range(GRID_SIZE):
            cell = Cell(i, j)  # Создаем объект ячейки с координатами строки i и столбца j
            grid[i].append(cell)  # Помещаем ячейку в текущую строку матрицы
    return grid  # Возвращаем созданную матрицу


def draw_grid(win):
    """Чертит поверх ячеек серые линии сетки для визуального разделения."""
    for i in range(GRID_SIZE):
        # Рисуем горизонтальные линии
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        # Рисуем вертикальные линии
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))


def draw(win, grid):
    """Отрисовывает все элементы окна в рамках одного кадра."""
    win.fill(WHITE)  # Полностью очищаем холст, заливая его белым фоном
    for row in grid:
        for cell in row:
            cell.draw(win)  # Каждая ячейка самостоятельно отрисовывает свой квадрат
    draw_grid(win)  # Наносим поверх сетку серых линий
    pygame.display.update()  # Обновляем экран, чтобы изменения отобразились пользователю


def variant_17(grid):
    """Реализуем лабиринт 17 варианта."""
    # Полностью сбрасываем состояние всех ячеек перед загрузкой схемы
    for row in grid:
        for cell in row:
            cell.reset()

    # Задаем жесткие координаты для Старта и Финиша (в соответствии со схемой)
    start = grid[1][0]  # Синяя корона располагается на строке index 1, столбце index 0
    end = grid[9][9]    # Красный крест (финиш) располагается на строке index 9, столбце index 9

    start.make_start()  # Окрашиваем старт в оранжевый цвет
    end.make_end()      # Окрашиваем финиш в бирюзовый цвет

    # Множество кортежей координат препятствий (строка, колонка) по Варианту №17
    barriers = {(0, 1), (0, 6), (1, 2), (1, 6), (2, 2), (3, 4), (3, 7), (3, 8), (4, 1), (4, 5), (4, 9), (5, 0), (5, 2), (5, 3), (5, 5), (5, 6), (5, 8), (6, 0), (6, 1), (6, 3), (6, 5), (7, 0), (7, 4), (7, 9), (8, 0), (8, 2), (8, 3), (8, 9), (9, 2), (9, 5), (9, 7)}

    # Превращаем выбранные координаты в черные непроходимые ячейки препятствий
    for r, c in barriers:
        grid[r][c].make_barrier()

    return start, end  # Возвращаем объекты старта и финиша


def main():
    """Основная функция."""
    grid = make_grid()  # Создаем базовую сетку объектов Cell
    start, end = variant_17(grid)  # Накладываем лабиринт Варианта 17

    run = True  # Флаг работы главного цикла программы
    while run:
        draw(WIN, grid)  # Постоянно отрисовываем актуальное состояние поля
        
        # Мониторим событя
        for event in pygame.event.get():
            # Если пользователь закрыл окно
            if event.type == pygame.QUIT:
                run = False  # Выходим цикла

            # Если пользователь клавишу
            if event.type == pygame.KEYDOWN:
                # Нажатие на "Пробел" запускает поиск пути
                if event.key == pygame.K_SPACE:
                    # Перед стартом алгоритма заставляем каждую ячейку обновить список своих соседей
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    # Вызываем функцию поиска пути алгоритмом A*
                    a_star_algorithm(lambda: draw(WIN, grid), grid, start, end)

                # Нажатие на "R" (английская раскладка) сбрасывает лабиринт к начальному состоянию
                if event.key == pygame.K_r:
                    start, end = variant_17(grid)  # Повторно загружаем схему Варианта 17

    pygame.quit()


if __name__ == "__main__":
    main()