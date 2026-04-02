import threading
import random
import time
import matplotlib.pyplot as plt

def quick_sort_t(arr, threads = 2):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    res_left = []
    res_right = []

    if threads >= 2 and len(arr) >= 10000:
        left_threads = threads // 2
        right_threads = threads // 2

        def sort_left():
            nonlocal res_left
            res_left = quick_sort_t(left, left_threads)

        def sort_right():
            nonlocal res_right
            res_right = quick_sort_t(right, right_threads)

        t1 = threading.Thread(target = sort_left)
        t2 = threading.Thread(target = sort_right)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
    else:

        res_left = quick_sort_t(left, 0)
        res_right = quick_sort_t(right, 0)

    return res_left + middle + res_right

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

sizes = [100, 1000, 10000, 20000, 30000, 40000, 50000]
quick_times = []
threaded_quick2_times = []
threaded_quick4_times = []
threaded_quick8_times = []

for size in sizes:
    data = [random.randint(0, 1000) for _ in range(size)]
    
    start = time.time()
    quick_sort(data)
    quick_times.append(time.time() - start)
    print(size, 'classic', time.time() - start)
    
    start = time.time()
    quick_sort_t(data, threads=2)
    threaded_quick2_times.append(time.time() - start)
    print(size, '2 threads', time.time() - start)

    start = time.time()
    quick_sort_t(data, threads=4)
    threaded_quick4_times.append(time.time() - start)
    print(size, '4 threads', time.time() - start)

    start = time.time()
    quick_sort_t(data, threads=8)
    threaded_quick8_times.append(time.time() - start)
    print(size, '8 threads', time.time() - start)

plt.figure(figsize=(10, 6))
plt.plot(sizes, quick_times, label='Обычная сортировка', marker='o')
plt.plot(sizes, threaded_quick2_times, label='Многопоточная (2 потока)', marker='o')
plt.plot(sizes, threaded_quick4_times, label='Многопоточная (4 потока)', marker='o')
plt.plot(sizes, threaded_quick8_times, label='Многопоточная (8 потоков)', marker='o')

plt.title('Сравнение времени сортировки с разным кол. потоков')
plt.xlabel('Размер массива')
plt.ylabel('Время выполнения')
plt.legend()
plt.show()
