from multiprocessing import Pool, cpu_count

from time import time
import logging


def factorize(*numbers: int):
    result = []
    max_processes = int(cpu_count() * 0.8)  # Максимальна кількість процесів

    pool = Pool(processes=min(max_processes, len(numbers)))

    for number in numbers:
        start_time_1 = time()
        factors = pool.apply_async(find_factors, (number,))
        end_time_1 = time()
        execution_time = end_time_1 - start_time_1
        result.append(factors.get())
        print(
            f'factorize({number}) starts at separate process | Duration: {execution_time} (sec) | Result : {factors.get()}')

    pool.close()
    pool.join()

    return result


def find_factors(number: int) -> list[int]:
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(treadName)s %(message)s")

    start_time = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end_time = time()
    execution_time_parallel = end_time - start_time
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    print(f'============================================== \n'
          f'End of program!\n'
          f'Execution time:, {execution_time_parallel}\n'
          f'Number of process: {int(cpu_count() * 0.8)}')
