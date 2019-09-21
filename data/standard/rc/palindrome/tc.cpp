#include<bits/stdc++.h>
#define ll long long
using namespace std;
int main()
{
	ll t;
	cin>>t;
	while(t--)
	{
		string s;
		cin>>s;
		ll flag=0;
		for(ll i=0;i<s.size()/2;i++)
		{
			if(s[i]!=s[s.size()-1-i])
			{
				flag=1;
			}
		}
		if(flag==1)
			cout<<"NO"<<endl;
		else
			cout<<"YES"<<endl;
	}
}