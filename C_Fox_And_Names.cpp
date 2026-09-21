#include <bits/stdc++.h>
using namespace std;
bool Cycle(int node,vector<bool>&vis,vector<bool>&pathVis,vector<vector<int>>&adj,stack<int>&st){
    vis[node]=true;
    pathVis[node]=true;
    for(auto it:adj[node]){
        if(!vis[it]){
            if(Cycle(it,vis,pathVis,adj,st)){
                return true;
            }
        }
        else if(pathVis[it]){
            return true;
            //cycle exist
        }
    }
    st.push(node);
    pathVis[node]=false;
    return false;
};
int main() {
    int m;
    cin>>m;
    vector<string> st(m);
    for(int i=0;i<m;i++){
        cin>>st[i];
    }
    // now we will have the 26 string in whihc we will have the adjacency matrix
    vector<vector<int>>adj(26);
    for(int i=0;i<m-1;i++){
        bool found=false;
        for(int j=0;j<min(st[i].size(),st[i+1].size());j++){
            // if the charcter are differrnt then this measn that they the  order of the second is gerater 
            if(st[i][j]!=st[i+1][j]){
                // then we will link them 
                found=true;
                adj[st[i][j]-'a'].push_back(st[i+1][j]-'a');
                break;
            } 
        }
        if(!found && (st[i].size()>st[i+1].size())){
            cout<<"Impossible"<<endl;
            return 0;
        } 
    }
    // now we will call the cycle then we will check and call alll the nodes if the cycle exists then we will return Impossiibele
    //else we will empty the stack and return what we will get
    vector<bool>vis(26);
    vector<bool>pathVis(26);
    stack<int>stk;
    bool cycle = false;
    for(int i=0;i<26;i++){
        if(!vis[i]){
            if(Cycle(i,vis,pathVis,adj,stk)){
                cycle=true;
            }
        }
    }
    if(cycle){
        cout<<"Impossible"<<endl;
        return 0;
    }
    string ans="";
    while(!stk.empty()){
        ans+=stk.top()+'a';
        stk.pop();
    }
    cout<<ans<<endl;
    return 0;
}