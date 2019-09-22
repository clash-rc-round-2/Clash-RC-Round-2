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
ll fpow(ll x,ll y){x=x%MOD;ll res=1;while(y){if(y&1)res=res*x;res%=MOD;y=y>>1;x=x*x;x%=MOD;}return res;}
ll inv(ll a,ll m){ll c=m;ll y=0,x=1;if(m==1)return 0;while(a>1){ll q=a/m;ll t=m;m=a%m,a=t;t=y;y=x-q*y;x=t;}if(x<0)x+=c;return x;}
int main(){
    ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);
    ll t;
    cin>>t;
    while(t--){
    ll n,m;
    map<ll,ll>m1,m2;
    map<ll,ll>::iterator it;
    cin>>n;
    for(int i=0;i<n;i++)
    {
        ll x;
        cin>>x;
        m1[x]++;
    }
    cin>>m;
    for(int i=0;i<m;i++)
    {
        ll x;
        cin>>x;
        m2[x]++;
    }
    ll res=0;
    for(it=m1.begin();it!=m1.end();it++)
    {
        if(m2[it->f-1])
        {
            ll tmp=min(it->se,m2[it->f-1]);
            res+=tmp;
            it->se-=tmp;
            m2[it->f-1]-=tmp;
            
                
        }
        if(m2[it->f])
        {
             ll tmp=min(it->se,m2[it->f]);
            res+=tmp;
            it->se-=tmp;
            m2[it->f]-=tmp;
        }
        if(m2[it->f+1])
        {
             ll tmp=min(it->se,m2[it->f+1]);
            res+=tmp;
            it->se-=tmp;
            m2[it->f+1]-=tmp;
        }
            
    }
    cout<<res<<"\n";
}
}