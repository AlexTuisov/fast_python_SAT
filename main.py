# import numpy as np
# import time
# from numba import njit
import argparse


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solver settings')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    parser.add_argument('--o', )
    args = parser.parse_args()
    print(args.accumulate(args.integers))

    main()
