#include<bits/stdc++.h>
using namespace std;

int main()
{
	srand(time(0));

	int t=1000;
	cout<<t<<"\n";
	
	while(t--)
	{
		long long int x = rand()%(1000000000000000000);
		cout<<x<<"\n";
	}
	
	return 0;
}
