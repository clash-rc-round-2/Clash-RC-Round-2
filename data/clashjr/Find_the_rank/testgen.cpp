#include<bits/stdc++.h>
#define ll long long
using namespace std;
int main()
{
	srand(time(NULL));
	ll t=10;
	cout<<t<<"\n";
	while(t--)
	{
		ll a=rand()%99999+1;
		ll b=rand()%99999+1;
		ll c=rand()%99999+1;
		ll d=rand()%99999+1;
		cout<<a<<" "<<b<<" "<<c<<" "<<d<<"\n";
		ll q=9999+1;
		cout<<q<<"\n";
		while(q--)
		{
			cout<<(rand()%(ll)pow(10,12))+1<<"\n";
		}

	}
}