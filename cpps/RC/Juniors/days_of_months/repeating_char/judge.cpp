#include<bits/stdc++.h>
using namespace std;

int main()
{
	string s;
	cin>>s;
	
	for(int i=0;i<s.length();i++)
      	assert(s[i]<='z' && s[i]>='a');
	
	int small[26]={0},big[26]={0},count=0;
	
	for(int i=0;i<s.length();i++)
	{
	      if(s[i]<='z' && s[i]>='a')
      	      small[s[i]-'a']++;	     
      }
      
      for(int i=0;i<26;i++)
      {
            if(small[i]>1)
                  count++;           
      }
      
      cout<<count<<"\n";
}
