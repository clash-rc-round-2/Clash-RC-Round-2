#include<bits/stdc++.h>
#define mp make_pair
#define f first
#define se second
#define pb push_back
#define ms memset
#define MOD 1000000007
#define sp fixed<<setprecision
#define sz sizeof
#define all(x) x.begin(),x.end()
#define rall(x) x.rbegin(),x.rend()
using namespace std;
typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;
bool pr[1000007];
void sieve(){pr[0]=1;pr[1]=1;for(int i=2;i*i<(1000007);i++){for(int j=2*i;j<=1000007;j+=i){pr[j]=1;}}}
ll fpow(ll x,ll y){x=x%MOD;ll res=1;while(y){if(y&1)res=res*x;res%=MOD;y=y>>1;x=x*x;x%=MOD;}return res;}
ll findTrailingZeros(ll n) 
{ 
    // Initialize result 
    ll count = 0; 
  
    // Keep dividing n by powers of  
    // 5 and update count 
    for (ll i = 5; n / i >= 1; i *= 5) 
        count += n / i; 
  
    return count; 
} 
 
int main(){
	ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0); 
	ll x;
	cin>>x;
	cout<<findTrailingZeros(x);

}
