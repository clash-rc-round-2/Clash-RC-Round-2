#include<bits/stdc++.h>
#define ll long long
#define forr(i,p,n) for(ll i=p;i<n;i++)
using namespace std;
void printsum(ll mat[][1005],ll n,ll k) 
{ 
   if (k > n) return; 
   ll stripSum[n][n]; 
  
   for (ll j=0; j<n; j++) 
   { 
       ll sum = 0; 
       for (ll i=0; i<k; i++) 
          sum += mat[i][j]; 
       stripSum[0][j] = sum; 
       for (ll i=1; i<n-k+1; i++) 
       { 
            sum += (mat[i+k-1][j] - mat[i-1][j]); 
            stripSum[i][j] = sum; 
       } 
   } 
  for (ll i=0; i<n-k+1; i++) 
   { 
      ll sum = 0; 
      for (ll j = 0; j<k; j++) 
           sum += stripSum[i][j]; 
      cout << sum << "  "; 
  	  for (ll j=1; j<n-k+1; j++) 
      { 
         sum += (stripSum[i][j+k-1] - stripSum[i][j-1]); 
         cout << sum << "  "; 
      } 
  
      cout << "\n"; 
   } 
} 
int main()
{
	ll t;
	cin>>t;
	while(t--)
	{
		ll n;

		cin>>n;
		ll arr[n][1005];
		forr(i,0,n)
		{
			forr(j,0,n)
			{
				cin>>arr[i][j];
			}
		}
		ll q;
		cin>>q;
		forr(i,0,q)
		{
			ll k;
			cin>>k;
			printsum(arr,n,k);
		}

	}
}
