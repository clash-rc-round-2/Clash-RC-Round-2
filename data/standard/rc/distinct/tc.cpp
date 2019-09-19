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
		map<char,ll>m;
		ll ct=0;
		for(ll i=0;i<s.size();i++)
		{	
			m[s[i]]++;
			if(m[s[i]]==1)
			{
				ct++;
			}
		}
		cout<<ct<<endl;
	}
}