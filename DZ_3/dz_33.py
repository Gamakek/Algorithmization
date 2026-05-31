import time
import random
import matplotlib.pyplot as plt

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def radix_sort(arr):
    if not arr: return arr
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        count = [0] * 10
        output = [0] * len(arr)
        for num in arr:
            index = (num // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        i = len(arr) - 1
        while i >= 0:
            num = arr[i]
            index = (num // exp) % 10
            output[count[index] - 1] = num
            count[index] -= 1
            i -= 1
        for i in range(len(arr)):
            arr[i] = output[i]
        exp *= 10
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


if __name__ == "__main__":
    sizes = [100, 300, 500, 700, 1000, 1300, 1500]

    results = {
        "Пузырьком": [],
        "Быстрая": [],
        "Поразрядная": []
    }

    for size in sizes:
    
        base_array = [random.randint(1, 10000) for _ in range(size)]
    
        arr_copy = base_array.copy()
        start = time.perf_counter()
        bubble_sort(arr_copy)
        results["Пузырьком"].append(time.perf_counter() - start)
        print('Пузырьком', time.perf_counter() - start, size)

        arr_copy = base_array.copy()
        start = time.perf_counter()
        quick_sort(arr_copy)
        results["Быстрая"].append(time.perf_counter() - start)
        print('Быстрая', time.perf_counter() - start, size)

        arr_copy = base_array.copy()
        start = time.perf_counter()
        radix_sort(arr_copy)
        results["Поразрядная"].append(time.perf_counter() - start)
        print('Поразрядная', time.perf_counter() - start, size)

    plt.figure(figsize=(12, 7))

    for algo_name, times in results.items():
        plt.plot(sizes, times, marker='o', label=algo_name)

    plt.title("Сравнение времени работы алгоритмов сортировки")
    plt.xlabel("Количество элементов в массиве (n)")
    plt.ylabel("Время выполнения (секунды)")
    plt.legend()
    plt.grid(True)
    plt.yscale("linear")

    plt.show()
