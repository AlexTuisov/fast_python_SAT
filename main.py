import numpy as np
import time
from numba import njit


def main():
    pass

    # start = time.time()
    # numpy_speed_check(2)
    # numpy_speed_check(1000)
    # end = time.time()
    # print(f"Elapsed time: {end-start:.2f} seconds")


# @njit(fastmath=True, parallel=True)
# def numpy_speed_check(n):
#     a = np.random.random((n, n, n))
#     b = np.extract(a > 0.999, a)
#     print(len(b))


if __name__ == '__main__':
    main()
