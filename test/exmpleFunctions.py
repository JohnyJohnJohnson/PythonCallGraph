# Some Example functions

# fibonaci

def fib(i):
    if i<=2:
        return 1
    return fib(i-1)+fib(i-2)


# binomial coificients

def binom(n,k):
    if k==1:
        return 1
    if k == n:
        return 1
    return binom(n-1,k-1) + binom(n-1,k)


# LCS

