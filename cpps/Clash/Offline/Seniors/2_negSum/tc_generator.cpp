#include<bits/stdc++.h>
#define ll long long
using namespace std;
int main()
{
	srand(time(0));
	ll t = rand()%6 + 5;
	cout << t << "\n";
	while(t--)
	{
		ll n = rand()%100 + 1;
		ll q = rand()%1000 + 1;
		ll sum = 0;
		//cout << n << " " << q << "\n";
		vector<ll>a;
		for(int i=0;i<n;i++)
		{
			ll temp = rand()%100000 + 1;
		//	cout << temp << " ";
			//sum+=temp;
			ll ti = rand()%1000 + 1;
			//ll ti = 1;
			for(int j=0;j<ti;j++)
			{
				a.push_back(temp);
				sum+=temp;
			}
		}
		n = a.size();
		ll type = rand()%2;
		if(type)
		{
			sort(a.begin(),a.end());
			reverse(a.begin(),a.end());
		}
		//cout << a.size() << "\n";
		cout << n << " " << q << "\n"; 
		for(int i=0;i<a.size();i++)
			cout << a[i] << " ";
		cout << "\n";	
		while(q--)
		{
			ll x,typeq = rand()%3;
			if(typeq==0)
				x = rand()%sum + 100;
			else if(typeq==1)
				x = sum - a[rand()%n];
			else
				x = rand()%100000 + 1;
			cout << x << "\n";
		}
	}
}

