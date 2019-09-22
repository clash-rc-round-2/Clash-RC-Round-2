#include<bits/stdc++.h>
#define ll long long
#define pb push_back
#define mod 1000000007
using namespace std;
ll arr[1000005];
vector<ll> v;
void sieve()
{
	for(ll i=2;i<=1000000;i++)
	{
		if(arr[i]==0)
		{
			for(ll j=i*i;j<=1000000;j+=i)
			{
				arr[j]=1;
			}
		}
	}
	for(ll i=2;i<=1000000;i++)
	{
		if(arr[i]==0)
		{
			v.pb(i);
		}
	}
}
ll modadd(ll x,ll y)
{
	ll ans=((x%mod)+(y%mod))%mod;
	return ans;
}
ll modmul(ll x,ll y)
{
	ll ans=((x%mod)*(y%mod))%mod;
	return ans;
}
int main()
{
	sieve();
	ios_base::sync_with_stdio(0);
	cin.tie(NULL);
	ll t;
	cin>>t;
	while(t--)
	{
		ll n;
		cin>>n;
		ll count=1;
		for(ll i=0;i<v.size();i++)
		{
			if(v[i]<=n)
			{
				ll pow=v[i];
				ll cnt=0;
				ll n1=n;
				while(n1/pow!=0)
				{
					ll t1=n1/pow;
					cnt+=t1;
					pow=pow*v[i];
				}
				ll t1=((cnt+1)*(cnt+2)/2)%mod;
				count=modmul(count,t1);
			}
		}
		cout<<count<<"\n";
	}
	return 0;
}