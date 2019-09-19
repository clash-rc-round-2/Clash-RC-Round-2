#include<bits/stdc++.h>
#define ios ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
#define ll long long
#define hell 1000000007
#define hell2 1000000006
#define pb push_back
#define x first
#define y second
using namespace std;
vector<ll>z;
void zfunc(string s)// calculates z value at index i such that maximum prefix length for string p starting from index i
{
  ll sz = s.size();
  z.pb(-1);
  ll l=0,r=0;
  for(int i=1;i<sz;i++)
  {
    if(i>r)
    {
      l=i;
      r=i;
      while(r<sz && s[r-l]==s[r])
        r++;
      z.pb(r-l);
      r--;
    }
    else
    {
      ll k = i-l;
      if(z[k]<r-i+1)
        z.pb(z[k]);
      else
      {
        l=i;
        while(r<sz && s[r-l]==s[r])
          r++;
        z.pb(r-l);
        r--;
      }
    }
  }
}
int main(){
	ios
	ll t;
	cin >> t;
  	//t = 1;
	while(t--){
      z.clear();
      ll n;
      cin >> n;
      string s;
      cin >> s;
      vector<ll>cnt(n+1,0);
      zfunc(s);
      for(int i=1;i<n;i++)
      	cnt[z[i]]++;
      ll mx = 0;
      ll ind = 0;
      for(int i=n-1;i>=0;i--)
      	cnt[i]+=cnt[i+1];
      /*for(int i=0;i<=n;i++)
      	cout << cnt[i] << " ";*/
      for(int i=1;i<=n;i++)
      {
      //	cout << cnt[i] << " ";
      	if(cnt[i]>=mx)
      	{
      		mx = cnt[i];
      		ind = i;
      	}
      }
      /*for(int i=0;i<n;i++)
      	cout << z[i] << " ";
      cout << "\n";*/
      for(int i=0;i<ind;i++)
      	cout << s[i];
      cout << "\n";
	}
}
