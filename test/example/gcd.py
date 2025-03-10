#!/usr/bin/env python3
"""Greatest Common Divisor

Some characterstics of this program used for testing check_args() does
not have a 'return' statement.

check_args() raises an uncaught exception when given the wrong number
of parameters.

"""
import sys


def check_args():
    if len(sys.argv) != 3:
        # Rather than use sys.exit let's just raise an error
        raise Exception(f"Need to give two numbers; got: {sys.argv}")
    for i in range(2):
        try:
            sys.argv[i + 1] = int(sys.argv[i + 1])
        except ValueError:
            print(f"** Expecting an integer, got: {repr(sys.argv[i])}")
            sys.exit(2)
        pass


def gcd(a, b):
    """GCD. We assume positive numbers"""

    # Make: a <= b
    if a > b:
        (a, b) = (b, a)
        pass

    if a <= 0:
        return None
    if a == 1 or b - a == 0:
        return a
    return gcd(b - a, a)


if __name__ == "__main__":
    check_args()

    (a, b) = sys.argv[1:3]
    print(f"The GCD of {a} and {b} is {gcd(a, b)}")
    pass
