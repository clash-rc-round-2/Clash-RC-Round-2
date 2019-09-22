#include<bits/stdc++.h>
using namespace std;
#define ll long long

void dfs(ll a,bool visited[],vector<ll> adj[],ll &count){
  visited[a]=true;
    count++;
  for(ll i=0;i<adj[a].size();++i){
    if(visited[adj[a][i]]==false){
      dfs(adj[a][i],visited,adj,count);
    }
  }
}
bool lessThan(vector<ll>v,ll x){
  ll sum=0;
  for(ll i=0;i<v.size();i++){
    sum+=(x+i)*v[i];
  }
  return sum<=1000000000;
}
ll binary(vector<ll> v){
  ll low=0;
  ll high=1000000000;
  ll res=0;
  while(low<=high){
    ll mid=(low+high)/2;
    if(lessThan(v,mid)){
    res=max(res,mid);
    low=mid+1;
  }
  else{
    high=mid-1;
  }
  }
  return res;
}
int main(){
  ll testcase;
  cin>>testcase;
  while(testcase--){
    ll n,m;
    cin>>n>>m;
    bool visited[n+1];
    vector<ll>adj[n+1];
    vector<ll>v;
    for(ll i=0;i<m;i++){
      ll a,b;
      cin>>a>>b;
      adj[a].push_back(b);
      adj[b].push_back(a);
    }
      memset(visited,0,n+1);
      for(ll i=0;i<n;i++){
        ll count=0;
        if (visited[i]==false){
          dfs(i,visited,adj,count);
          v.push_back(count);
        }
      }
      sort(v.begin(),v.end());
      cout<<binary(v)<<endl;
    }
}
