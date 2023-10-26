import sys
import math
from functools import cache
from timeit import default_timer as timer

def time_function(func: callable):
    def __inner(*args, **kwargs):
        s = timer()
        r = func(*args, **kwargs)
        return r, timer() - s
    return __inner

# Lazy implementation
def factorial(n: int):
    return 1 if n <= 1 else n * factorial(n - 1)

def pascal(n: int, k: int):
    if k == 0:
        return 1
    elif k > n:
        return 0
    return pascal(n - 1, k - 1) + pascal(n - 1, k)

@cache
def pascal_memoization(n: int, k: int):
    if k == 0:
        return 1
    elif k > n:
        return 0
    return pascal_memoization(n - 1, k - 1) + pascal_memoization(n - 1, k)


class BinomialCoefficient:
    USE_CACHING = True
    
    @time_function
    @staticmethod
    def explicit(n: int, k: int):
        return factorial(n) / (factorial(k)*(factorial(n-k)))

    @time_function
    @staticmethod
    def recursive(n: int, k: int, cached = False):
        if BinomialCoefficient.USE_CACHING:
            return pascal_memoization(n, k)
        return pascal(n, k)

    @time_function
    @staticmethod
    def approximately(n: int, k: int):
        if k == 0 or k == n:
            return 1
        else:
            return math.sqrt(n/(2*math.pi*k*(n-k)))*(n**n/(k**k*(n-k)**(n-k))) 

    
def calculate_all_terms(func: callable, n: int):
    results = dict()
    for i in range(1, n + 1):
        for j in range(i + 1):
            results[(i, j)] = func(i, j)
    return results

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) == 2 else 20
    
    BinomialCoefficient.USE_CACHING = False
    
    res_explicit = calculate_all_terms(BinomialCoefficient.explicit, N)
    res_recursive = calculate_all_terms(BinomialCoefficient.recursive, N)
    res_approximately = calculate_all_terms(BinomialCoefficient.approximately, N)
    
    # Rechenzeit
    print(f"[ === LAUFZEIT (n = {N}) === ]")
    print(f"Explizit: {sum(v[1] for v in res_explicit.values()):.6f}s")
    print(f"Rekursiv: {sum(v[1] for v in res_recursive.values()):.6f}s")
    print(f"Approximativ: {sum(v[1] for v in res_approximately.values()):.6f}s")
    
    # Laufzeitabhängigkeit (Skalierbarkeit)
    
    # Relativer Fehler