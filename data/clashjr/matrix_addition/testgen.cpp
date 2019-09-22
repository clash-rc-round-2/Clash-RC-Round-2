#include<bits/stdc++.h>
#define ll long long
#define forr(i,p,n) for(ll i=p;i<n;i++)
using namespace std;
int main()
{
	ll t=10;
	cout<<t<<"\n";
	srand(time(NULL));
	forr(i,0,t)
	{
		ll n=rand()%99+1;
		cout<<n<<"\n";
		forr(i,0,n)
		{
		forr(j,0,n)
		{
			cout<<rand()%((ll)pow(10,9))<<" ";
		}
		cout<<"\n";
		}
		ll q=101;
		cout<<q<<"\n";
		forr(i,0,q)
		{
			ll k=rand()%(n-1)+1;
			cout<<k<<"\n";
		}

	}

}