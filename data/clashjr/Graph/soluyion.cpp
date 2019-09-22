#include<bits/stdc++.h>
 #define mp make_pair
 #define f first
 #define se second
 #define pb push_back
 #define ms memset
 #define MOD 1000000007
 #define sp fixed<<setprecision
 #define sz sizeof
 #define all(v) v.begin(),v.end()
 #define rall(v) v.rbegin(),v.rend()
 using namespace std;
 typedef long long ll;
 typedef unsigned long long ull;
 typedef long double ld;
 ll sieve(ll n){bool pr[1000007];ms(pr,true,sz(pr) ); ll count=0;for(int i=2;i*i<n;i++){if(pr[i]==true){for(int j=i*2;j<=n;j+=i){pr[j]=false;}}}for(ll i=2;i<n;i++){if(pr[i]){count++;}}return count;}
 ll fpow(ll x,ll y){x=x%MOD;ll res=1;while(y){if(y&1)res=res*x;res%=MOD;y=y>>1;x=x*x;x%=MOD;}return res;}
 struct A{

ll matrix[101][101];
A(){
memset(matrix,0,sizeof(matrix));}
};
ll n=0;
A  matrix_mult(A obj1, A obj2){
  A obj3;

  for (ll i=1;i<=n;i++){
    for(ll j=1;j<=n;j++){
      for(ll k=1;k<=n;k++){
      obj3. matrix[i][k] = (obj3.matrix[i][k] + obj1.matrix[i][j] * obj2.matrix[j][k])%1000000007;
      }
      }
    }
  return obj3;
}

A fast_exponentiation( A obj1, ll k){
  if( k == 1)
    return obj1;
  else{
    if (k % 2 == 0)
    {  A obj2 = fast_exponentiation( obj1, k/2);
      return matrix_mult(obj2, obj2);
    }
    else
      return matrix_mult(obj1, fast_exponentiation(obj1, k - 1));
}
}
 int main()
 {
 ios_base::sync_with_stdio(false);
  cin.tie(NULL);
ll k,e;
cin>>k>>n>>e;
A obj1;
for(ll i=1;i<=e;i++){
 ll a,b;
 cin>>a>>b;
 obj1.matrix[a][b]=1;
}

A obj2=fast_exponentiation(obj1,k);
            ll Q=0;
            cin>>Q;
            for(ll i=0;i<Q;i++){

              ll a,b;
              cin>>a>>b;
              cout<<obj2.matrix[a][b]%1000000007<<"\n";
            }
 return 0;
 }

