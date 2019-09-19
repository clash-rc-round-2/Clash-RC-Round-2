import random;
r1 = random.randint(1,100);
print(r1);
for i in range(r1):
	s="";
	r2 = random.randint(1,25)
	for i in range(r2):
		r3 = random.randint(1,25);
		s+=chr(ord('a')+r3)
	print(s)