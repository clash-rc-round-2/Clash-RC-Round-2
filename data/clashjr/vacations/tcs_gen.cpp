#include<bits/stdc++.h>
# define ll long long
using namespace std;
int randomize()  
{    
    return 1+(rand() % 1000000);  
} 
int main(){
    ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);

srand(time(0));
ll t=30;
cout<<t<<"\n";
while(t--){

ll n=1+(rand() % 10000);
ll m=1+(rand() % 10000);
cout<<n<<"\n";

vector<int> v1(n),v2(m); 
generate(v1.begin(), v1.end(), randomize);
generate(v2.begin(), v2.end(), randomize);
for(int i=0;i<v1.size();i++) cout<<v1[i]<<" ";
cout<<"\n";
cout<<m<<"\n";
for(int i=0;i<v2.size();i++) cout<<v2[i]<<" ";
cout<<"\n";



}
}