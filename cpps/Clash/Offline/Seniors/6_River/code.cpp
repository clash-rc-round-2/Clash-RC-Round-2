#include<bits/stdc++.h>
#define ios ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
#define ll long long
#define hell 1000000007
#define hell1 1000000006
#define pb push_back
#define x first
#define y second
#define all(v) v.begin(),v.end()
#define MAXL 1000005
using namespace std;
vector<ll>adj[200005],visited(200005,0);
ll hackenbush(ll src)
{
	ll result = 0;
	visited[src] = 1;
	for (int i = 0; i < adj[src].size(); i++)
		if(!visited[adj[src][i]])
			result^=(hackenbush(adj[src][i])+1);
	return result;
}
int main(){
	//ios
	ll t;
	cin >> t;
	while(t--){
		for(int i=0;i<200005;i++)
		{
			adj[i].clear();
			visited[i] = 0;
		}
		
		ll n;
		cin >> n;
		//cout << n << "\n";
		for(int i=0;i<n;i++)
		{
			ll l,r;
			cin >> l >> r;
			adj[l].pb(r);
		}
        ll result = hackenbush(0);
        string player1="Harshit",player2="Varad";
        //cout << result << "\n";
        if(result)
        	cout << player1 << "\n";
        else
        	cout << player2 << "\n";
	}
}
