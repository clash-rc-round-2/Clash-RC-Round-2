from random import randint as r 
t = r(100,100000)
print(t)
a = []
b = []
for i in range(t):
    a.append(r(1,1000000))
    b.append(r(1,1000000))
print(*a)
print(*b)