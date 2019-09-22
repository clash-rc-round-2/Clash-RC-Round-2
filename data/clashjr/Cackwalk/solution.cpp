#include<bits/stdc++.h>
#define ll long long
using namespace std;
int main()
{
	ll n,ct=0;
	cin>>n;
	ll a[n],b[n];
	for(ll i=0;i<n;i++)
	{
		cin>>a[i];
	}
	for(ll i=0;i<n;i++)
		cin>>b[i];
	for(ll i=0;i<n;i++)
	{
		if(a[i]!=b[i])
			ct++;
	}
	cout<<ct<<endl;
}