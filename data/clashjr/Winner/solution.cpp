#include<iostream>
#define T 100000
#define ll long long
#define mod 1000000007
using namespace std;
ll fact[10000007];
void facti(){
	fact[0] = 1;
	for(int i = 1;i < 10000007;i++){
		fact[i] = (fact[i - 1] * i) % mod;
	}
}
ll xyp(ll x,ll y){
	if(y == 0) return 1LL;
	if(y == 1) return x;
	if(y % 2){
		ll p = xyp(x,y - 1);
		return (x * p) % mod;
	}
	ll p = xyp(x,y / 2);
	return (p * p) % mod;
}
ll inv(ll n){
	return xyp(n,mod - 2);
}
ll ncr(ll n,ll r){
	return ((fact[n] * inv(fact[r]) % mod) * inv(fact[n - r]) % mod)% mod;
}
int main(){
	ll t;
	cin >> t;
	facti();
	while(t--){
		ll n,k,m;
		cin >> n >> k >> m;
		ll p = ncr(m + k - 1,m - 1);
		ll q = ncr(m + n,m);
		q = inv(q);
		cout << (p * q) % mod << "\n";
	}	
	return 0;
}
