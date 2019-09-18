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
const int ALPHABET_SIZE = 26;
ll cnt = 0;
vector< pair<ll,ll> >gr;
struct TrieNode
{
    struct TrieNode *children[ALPHABET_SIZE];
    bool isEndOfWord;
};
struct TrieNode *getNode(void)
{
    struct TrieNode *pNode =  new TrieNode;
 
    pNode->isEndOfWord = false;
 
    for (int i = 0; i < ALPHABET_SIZE; i++)
        pNode->children[i] = NULL;
 
    return pNode;
}
void insert(struct TrieNode *root, string key)
{
    struct TrieNode *pCrawl = root;
 
    for (int i = 0; i < key.length(); i++)
    {
        int index = key[i] - 'a';
        if (!pCrawl->children[index])
            pCrawl->children[index] = getNode();
 
        pCrawl = pCrawl->children[index];
    }
    pCrawl->isEndOfWord = true;
}
bool search(struct TrieNode *root, string key)
{
    struct TrieNode *pCrawl = root;
 
    for (int i = 0; i < key.length(); i++)
    {
        int index = key[i] - 'a';
        if (!pCrawl->children[index])
            return false;
 
        pCrawl = pCrawl->children[index];
    }
 
    return (pCrawl != NULL && pCrawl->isEndOfWord);
}
ll hackenbush(struct TrieNode *par,ll cnt2 = 0)
{
	ll result = 0;
	for (int i = 0; i < ALPHABET_SIZE; i++)
		if(par->children[i] != NULL)
			result^=(hackenbush(par->children[i],cnt)+1);
	return result;
}
void dfs(struct TrieNode *par,ll pid)
{
	for(int i=0;i<26;i++)
		if(par->children[i]!=NULL)
		{
			cnt++;
			gr.pb({pid,cnt});
			dfs(par->children[i],cnt);
		}
}
int main(){
	ios
	ll t;
	cin >> t;
	cout << t << "\n";
	while(t--){
		ll n;
		cin >> n;
		vector<string>dict(n);
		for(int i=0;i<n;i++)
			cin >> dict[i];
		struct TrieNode *root = getNode();
    	for (int i = 0; i < n; i++)
        	insert(root, dict[i]);
        cnt = 0;
        gr.clear();
        dfs(root,0);
       cout << cnt << "\n";
       for(auto e:gr)
       		cout << e.x << " " << e.y << "\n";
	}
}
