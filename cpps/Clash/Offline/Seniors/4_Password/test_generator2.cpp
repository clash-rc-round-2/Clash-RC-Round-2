#include<bits/stdc++.h>
#define pb push_back
#define mp make_pair
#define mod 1000000007
#define ios ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);

typedef long long ll ;
typedef long double ld ;
typedef long long int lli;

using namespace std;
//reference: geeks
ll mult(ll a,ll b, ll p=mod){
	ll res = 0;
    a %= p;
    while (b)
    {
        if (b & 1)
            res = (res + a) % p;
    		a = (2 * a) % p;
        b >>= 1;
    }
    return res;
}
ll add(ll a, ll b, ll p=mod){return (a%p + b%p)%p;}
ll sub(ll a, ll b, ll p=mod){return (a%p - b%p + p)%p;}
ll fpow(ll n, ll k, ll p = mod) {ll r = 1; for (; k; k >>= 1) {if (k & 1) r = mult(r,n,p); n = mult(n,n,p);} return r;}
ll inv(ll a, ll p = mod) {return fpow(a, p - 2, p);}

ll getRandoms(ll lower, ll upper)
{
    //between lower and upper inclusive
    ll num = (rand() %
           (upper - lower + 1)) + lower;
return num;
}
int main()
{
	srand(time(0));
	int t=100,T;
	cout<<t<<"\n";
	T=t;
	//string s;
	//cin>>s;
	//cout<<s.length();
	while(t--)
	{
		string s="";
		ll n=getRandoms(50,100);
		n=10;//max len of prefix initially that will be the ans to the question
		for(int i=0;i<n;i++)
			s+=char(rand()%5+'a');
		ll len=n;
		ll j=getRandoms(2,n-2); //min length prefix to e concatenated
		while(len<100000)
		{
			ll i=getRandoms(j,n-1);
			if(len+i+1>100000)
				break;
			len+=i+1;
			s+=s.substr(0,i+1);	//concat
		}
		ll N=s.length();
		cout<<N<<"\n";
		cout<<s<<"\n";
	}


}
