#include<bits/stdc++.h>
#define ll long long
using namespace std;
int main()
{
	ll arr[10];
	arr[0]=0;
	arr[1]=0;
	arr[2]=2;
	arr[3]=3;
	arr[4]=2;
	arr[5]=5;
	arr[6]=5;
	arr[7]=7;
	arr[8]=2;
	arr[9]=3;
		string s;
		cin>>s;
		ll sum=0;
		for(ll i=0;i<s.size();i++)
		{
			sum+=arr[s[i]-'0'];
		}
		cout<<sum<<endl;
}