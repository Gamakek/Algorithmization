import random

def monte_carlo_area(rx_1, rx_2, ry_1, ry_2, num_points=20000000):
    inside_points = 0
    for _ in range(num_points):
        x = random.uniform(rx_1, rx_2)
        y = random.uniform(ry_1, ry_2)
        if (y >= (x ** 3 - 12 * x ** 2 + 4)) and (y <= (-(x ** 3) + x ** 2 - 4)):
            inside_points += 1
    

    square_area = (rx_2 - rx_1) * (ry_2 - ry_1) 
    figure_area = (inside_points / num_points) * square_area
    return figure_area

# Пример использования:
rx_1 = 3 # Найменьшее значение x для прямоугольной области, в которой находится фигура
rx_2 = 6 # Наибольшее значение x для прямоугольной области, в которой находится фигура
ry_1 = -212 # Найменьшее значение y для прямоугольной области, в которой находится фигура
ry_2 = -22 # Наибольшее значение y для прямоугольной области, в которой находится фигура
estimated_area = monte_carlo_area(rx_1, rx_2, ry_1, ry_2)
print(f"Оцененная площадь: {estimated_area}")
