#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int K; double S_cost, latency_ms, bandwidth_gbps;
    long long bytes_per_token; int num_layers;
    cin >> K >> S_cost >> latency_ms >> bandwidth_gbps >> bytes_per_token >> num_layers;

    double SLO1, SLO2, tp_UB, tp_base, dist_base, w_tp, w_c;
    cin >> SLO1 >> SLO2 >> tp_UB >> tp_base >> dist_base >> w_tp >> w_c;

    int N; cin >> N;
    for(int i=0;i<N;i++){
        long long bs; double a,b,c,d,e,f;
        cin >> bs >> a >> b >> c >> d >> e >> f;
    }

    deque<int> readyPPre;
    vector<deque<int>> readyPProc(K), readyDProc(K);
    deque<int> readyPPost, readyDPre, readyDPost;

    bool Ebusy = false;
    vector<bool> remoteBusy(K, false);
    int rrCounter = 0;

    vector<int> reqRemote;
    auto ensureSize = [&](int rid){
        if((int)reqRemote.size() <= rid) reqRemote.resize(rid+1, -1);
    };

    unordered_set<int> finishedSet;

    while(true){
        string tok;
        if(!(cin >> tok)) break;
        if(tok == "END") break;
        // tok is the timestamp (unused for our reactive scheduler)

        int e; cin >> e;
        vector<int> justDPostRids;

        for(int i=0;i<e;i++){
            string kind; cin >> kind;
            if(kind == "ARR"){
                int rid; long long lin;
                cin >> rid >> lin;
                ensureSize(rid);
                readyPPre.push_back(rid);
            } else if(kind == "TDN"){
                string server; cin >> server;
                string a,b; cin >> a >> b;
                if(a=="P" && b=="PRE"){
                    int remote, rid; double dur;
                    cin >> remote >> rid >> dur;
                    Ebusy = false;
                } else if(a=="P" && b=="PROC"){
                    int ls,le,remote,rid; double dur;
                    cin >> ls >> le >> remote >> rid >> dur;
                    remoteBusy[remote] = false;
                } else if(a=="P" && b=="POST"){
                    int remote, rid; double dur;
                    cin >> remote >> rid >> dur;
                    Ebusy = false;
                    readyDPre.push_back(rid);
                } else if(a=="D" && b=="PRE"){
                    int minus1,m; cin >> minus1 >> m;
                    vector<int> rids(m);
                    for(auto&x:rids) cin >> x;
                    double dur; cin >> dur;
                    Ebusy = false;
                } else if(a=="D" && b=="PROC"){
                    int remote,m; cin >> remote >> m;
                    vector<int> rids(m);
                    for(auto&x:rids) cin >> x;
                    double dur; cin >> dur;
                    remoteBusy[remote] = false;
                } else if(a=="D" && b=="POST"){
                    int minus1,m; cin >> minus1 >> m;
                    vector<int> rids(m);
                    for(auto&x:rids) cin >> x;
                    double dur; cin >> dur;
                    Ebusy = false;
                    for(int rid: rids) justDPostRids.push_back(rid);
                }
            } else if(kind == "XDN"){
                string dir; cin >> dir;
                int remote; long long size; string type; int m;
                cin >> remote >> size >> type >> m;
                vector<int> rids(m);
                for(auto&x:rids) cin >> x;
                if(dir=="UP" && type=="PRE"){
                    int rid = rids[0];
                    ensureSize(rid);
                    reqRemote[rid] = remote;
                    readyPProc[remote].push_back(rid);
                } else if(dir=="DOWN" && type=="PRE"){
                    readyPPost.push_back(rids[0]);
                } else if(dir=="UP" && type=="DEC"){
                    for(int rid: rids) readyDProc[remote].push_back(rid);
                } else if(dir=="DOWN" && type=="DEC"){
                    for(int rid: rids) readyDPost.push_back(rid);
                }
            } else if(kind == "FIN"){
                int rid; cin >> rid;
                finishedSet.insert(rid);
            }
        }

        for(int rid: justDPostRids){
            if(!finishedSet.count(rid)) readyDPre.push_back(rid);
        }

        vector<string> outLines;

        if(!Ebusy){
            if(!readyPPost.empty()){
                int rid = readyPPost.front(); readyPPost.pop_front();
                int remote = reqRemote[rid];
                outLines.push_back("E P POST " + to_string(remote) + " " + to_string(rid));
                Ebusy = true;
            } else if(!readyDPost.empty()){
                int rid = readyDPost.front(); readyDPost.pop_front();
                outLines.push_back("E D POST -1 1 " + to_string(rid));
                Ebusy = true;
            } else if(!readyDPre.empty()){
                int rid = readyDPre.front(); readyDPre.pop_front();
                outLines.push_back("E D PRE -1 1 " + to_string(rid));
                Ebusy = true;
            } else if(!readyPPre.empty()){
                int rid = readyPPre.front(); readyPPre.pop_front();
                int remote = rrCounter; rrCounter = (rrCounter+1) % K;
                ensureSize(rid);
                reqRemote[rid] = remote;
                outLines.push_back("E P PRE " + to_string(remote) + " " + to_string(rid));
                Ebusy = true;
            }
        }

        for(int k=0;k<K;k++){
            if(!remoteBusy[k]){
                if(!readyDProc[k].empty()){
                    int rid = readyDProc[k].front(); readyDProc[k].pop_front();
                    outLines.push_back("C" + to_string(k) + " D PROC " + to_string(k) + " 1 " + to_string(rid));
                    remoteBusy[k] = true;
                } else if(!readyPProc[k].empty()){
                    int rid = readyPProc[k].front(); readyPProc[k].pop_front();
                    outLines.push_back("C" + to_string(k) + " P PROC 0 " + to_string(num_layers) + " " + to_string(k) + " " + to_string(rid));
                    remoteBusy[k] = true;
                }
            }
        }

        cout << outLines.size() << "\n";
        for(auto &s : outLines) cout << s << "\n";
        cout << flush;
    }

    return 0;
}