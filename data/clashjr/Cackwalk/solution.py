n = int(input())
a = [int(x) for x in input().split()]
b = [int(x) for x in input().split()]
count = 0
for i in range(n):
    if(a[i]!=b[i]):
        count+=1
print(count)