
from libc.math cimport sqrt
from cpython cimport bool

cpdef bool is_divisible(int p, int q):
    return p % q == 0

cpdef list lower_divisors(int n):
    cdef int limit = int(sqrt(n)) + 1
    return [i for i in range(2, limit) if is_divisible(n, i)]

cpdef list divisors(int n):
    cdef list lower_divs = lower_divisors(n)
    return [1] + lower_divs + [n//i for i in reversed(lower_divs)]

