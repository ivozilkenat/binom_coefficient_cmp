import sys
import math
from functools import cache
from timeit import default_timer as timer

import matplotlib.pyplot as plt

def time_function(func: callable):
    def __inner(*args, **kwargs):
        s = timer()
        r = func(*args, **kwargs)
        return r, timer() - s
    return __inner

# Lazy implementation
def factorial(n: int):
    return 1 if n <= 1 else n * factorial(n - 1)

def factorial_stirling(n: int):
    if n == 0:
        return 1
    return math.sqrt(2*math.pi*n)*(n/math.e)**n

def pascal(n: int, k: int):
    if k == 0:
        return 1
    elif k > n:
        return 0
    return pascal(n - 1, k - 1) + pascal(n - 1, k)

@cache # Caches every call. Thus not bound to one starting (n, k)
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
    def recursive(n: int, k: int):
        if BinomialCoefficient.USE_CACHING:
            return pascal_memoization(n, k)
        return pascal(n, k)

    @time_function
    @staticmethod
    def approximately_equation(n: int, k: int):
        if k == 0 or k == n:
            return 1
        else:
            return math.sqrt(n/(2*math.pi*k*(n-k)))*(n**n/(k**k*(n-k)**(n-k))) 
        
    @time_function
    @staticmethod
    def approximately_stirling(n: int, k: int):
        return factorial_stirling(n) / (factorial_stirling(k)*(factorial_stirling(n-k)))

    
def calculate_all_terms(func: callable, n: int):
    results = dict()
    for i in range(1, n + 1):
        for j in range(i + 1):
            results[(i, j)] = func(i, j)
    return results

def get_runtime_from_results(results):
    runtime = [0 for _ in range(1, N + 1)]
    for ((n, _), (_, time)) in results.items():
        runtime[n - 1] += time
    return runtime

def get_error_from_results(norm_results, results):
    res_error = list()
    for n in range(1, N + 1):
        errors = list()
        for k in range(n + 1):
            result_approx = results[(n, k)][0]
            result_discrete = norm_results[(n, k)][0]
            errors.append(abs(result_discrete - result_approx) / result_discrete)
        res_error.append(sum(errors) / len(errors)) # errors are averaged
    return res_error

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) == 2 else 20
    
    BinomialCoefficient.USE_CACHING = True # Recursive function otherwise verryyy slowwwww
    
    res_explicit = calculate_all_terms(BinomialCoefficient.explicit, N)
    res_recursive = calculate_all_terms(BinomialCoefficient.recursive, N)
    res_approximately_eq = calculate_all_terms(BinomialCoefficient.approximately_equation, N)
    res_approximately_stirling = calculate_all_terms(BinomialCoefficient.approximately_stirling, N)

    # Rechenzeit
    print(f"[ === LAUFZEIT (n = {N}) === ]")
    print(f"Explizit: {sum(v[1] for v in res_explicit.values()):.6f}s")
    print(f"Rekursiv: {sum(v[1] for v in res_recursive.values()):.6f}s")
    print(f"Approximativ Gleichung: {sum(v[1] for v in res_approximately_eq.values()):.6f}s")
    print(f"Approximativ Stirling: {sum(v[1] for v in res_approximately_stirling.values()):.6f}s")
    
    x_values = [i for i in range(1, N + 1)]
    
    # Laufzeitabhängigkeit (Skalierbarkeit)
    
    runtime_explicit = get_runtime_from_results(res_explicit)
    runtime_approx_eq = get_runtime_from_results(res_approximately_eq)
    runtime_approx_stir = get_runtime_from_results(res_approximately_stirling)
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(
        x_values, 
        runtime_explicit, 
        label='runtime explicit'
    )
    plt.plot(
        x_values, 
        runtime_approx_eq, 
        label='runtime approx. equation'
    )
    plt.plot(
        x_values, 
        runtime_approx_stir, 
        label='runtime approx. Stirling'
    )
    
    plt.title('Comparing runtime for increasing n')
    plt.xlabel('n')
    plt.ylabel('runtime (seconds)')
    
    plt.legend()
    plt.grid(True)
           
    # Relativer Fehler
    plt.figure(figsize=(10, 6))
    
    errors_appox_eq = get_error_from_results(res_explicit, res_approximately_eq) 
    
    plt.plot(
        x_values,
        errors_appox_eq,
        label='avrg. error approx. equation'
    )
    
    plt.title('Comparing avrg. error for increasing n')
    plt.xlabel('n')
    plt.ylabel('avrg. error')
    
    plt.legend()
    plt.grid(True)
    plt.show()