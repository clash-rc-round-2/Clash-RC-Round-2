import random
r1 = random.randint(1,100);
print(r1)
x=0;
for i in range(r1):
	s="";
	r2 = random.randint(1,10000)
	for i in range(r2):
		r3 = random.randint(1,9);
		s+=chr(ord('0')+r3)
	x+=1;
	if(x%2==0):
		print(s+s[::-1])
	else:
		print(s);