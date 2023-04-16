n = int(input())
k = int(input())
a = n // k
b = n - a * (k - 1)
c = n - k + 1
print((k-1) * a * (a - 1) // 2 + b * (b - 1) // 2)
print(c * (c - 1) // 2)