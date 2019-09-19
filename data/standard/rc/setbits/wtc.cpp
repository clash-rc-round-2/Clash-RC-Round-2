#include<bits/stdc++.h>
#define ll long long
using namespace std;
int main()
{
		ll n,ct=0,pos=1;
		cin>>n;
		while(n)
		{
			ll r=n%2;
			n=n/2;
			if(r==1)
			{
				ct+=pos;
			}
			pos++;
		}
		cout<<ct<<endl;
}