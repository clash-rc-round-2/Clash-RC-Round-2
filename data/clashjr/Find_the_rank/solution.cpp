#include<bits/stdc++.h>
#define ll long long
#define forr(i,p,n) for(ll i=p;i<n;i++)
using namespace std;
int main()
{
    ll t;
    cin>>t;
    while(t--)
    {
        ll a,b,c,d;
        cin>>a>>b>>c>>d;
        ll arr[4];
        ll rank=0;
        arr[0]=a;
        arr[1]=b;
        arr[2]=c;
        arr[3]=d;
        sort(arr,arr+4);
        a=arr[0];
        b=arr[1];
        c=arr[2];
        d=arr[3];
        ll ab=((a*b)/__gcd(a,b));
        ll ac=((a*c)/__gcd(a,c));
        ll ad=((a*d)/__gcd(a,d));
        ll bc=((c*b)/__gcd(c,b));
        ll bd=((d*b)/__gcd(d,b));
        ll cd=((c*d)/__gcd(c,d));
        ll abc=(a*bc)/__gcd(a,bc);
        ll abd=(a*bd)/__gcd(a,bd);
        ll acd=(a*cd)/__gcd(a,cd);
        ll bcd=(b*cd)/__gcd(b,cd);
        ll abcd=(ab*cd)/__gcd(ab,cd);
        ll q;
        cin>>q;
        while(q--)
        {
            ll n;
            cin>>n;
            rank=0;
            rank+=n/a;
            rank+=n/b;
            rank+=n/c;
            rank+=n/d;
            rank-=n/ab;
            rank-=n/ac;
            rank-=n/ad;
            rank-=n/bc;
            rank-=n/bd;
            rank-=n/cd;
            rank+=n/abc;
            rank+=n/acd;
            rank+=n/bcd;
            rank+=n/abd;
            rank-=n/abcd;
            cout<<rank<<"\n";
        }
                
    }
}