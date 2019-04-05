# Dijkstra算法

Dijkstra算法用于解决单元最短路径问题。

算法伪代码：

```C++
// graph为图,数组distance为源点到达个点的最短路径长度,startPoint为起点
Dijkstra(Graph graph, vector<int> & distance, int startPoint) {
	初始化
	for(从1至n) {
		u = 使distance[u]最小的还没被访问的顶点的标号;
		记u已被访问;
		for(从u出发能到达的所有顶点v) {
			if(v未被访问 && 以u为中介使s到顶点v的最短距离distance[v]更优) {
				优化distanced[v];
			}
		}
	}
}

```

<br/>

## 邻接矩阵版

```C++
const int MAXV = 1000; // 最大顶点数
const int INF = 1000000000; // 设INF为一个极大的数

int n, Graph[MAXV][MAXV]; // n为顶点数,MAXV为最大顶点数
int distance[MAXV]; // 起点到达个点的最大un路径长度
bool isVisited[MAXV] = { false; } // isVisited[i] = ture 表示顶点i已访问

void Dijkstra(int start) { // s为起点
    fill(distance, distance + MAXV, INF);
    distance[start] = 0; // 起点s到达自身的距离为0

    for(int i = 0; i < n; i++) {
        int u = -1, MIN = INF; // u使d[u]最小, MIN存放该最小的distance[u]
        for(int j = 0; j < n; j++) {
            if(isVisited[j] == false && distance[j] < MIN) { // 找到未访问顶点中distance[]最小的
                u = j;
                MIN = distance[j];
            }
        }

        if(u == -1) return; // 找不到小于INF的distance[u], 说明剩下的顶点和起点s不联通
        isVisited[u] = true; // 标记u已被访问
        for(int v = 0; v < n; v++) {
            // 如果v未访问 且 u到达v 且以u为中介点可以使distance[v]更优
            if(isVisited[v] == false && Graph[u][v] != INF && distance[u] + Graph[u][v] < distance[v]) {
                distance[v] = distance[u] + Graph[u][v];
            }
        }
    }
}
```

## 邻接表版

```C++
const int MAXV = 1000; // 最大顶点数
const int INF = 1000000000; // 设INF为一个极大的数

struct Node {
    int v; // 目标顶点
    int dis; // dis
};
vector<Node> Adj[MAXV]; // 图Graph, Adj[u]存放从顶点u出发可以到达的所有顶点
int n; // n为顶点数
int distance[MAXV]; // 起点到达个点的最大un路径长度
bool isVisited[MAXV] = { false; } // isVisited[i] = ture 表示顶点i已访问

void Dijkstra(int start) {
    fill(distance, distance + MAXV, INF);
    distance[start] = 0; // 起点start到达自身的距离为0

    for(int i = 0; i < n; i++) {
        int u = -1, MIN = INF;  // 找到未访问顶点中distance[]最小的
        for(int j = 0; j < n; j++) {
            if(isVisited[j] == false && distance[j] < MIN) {
                u = j;
                MIN = distance[j];
            }
        }

        if(u == -1) return; // 找不到小于INF的distance[u], 说明剩下的顶点和起点s不联通
        isVisited[u] = true; // 标记u已被访问
        for(int j = 0; j < Adj[u].size(); j++) {
            int v = Adj[u][j].v; // 通过邻接表直接获取u所能到达的顶点v
            if(isVisited[v] = false && distance[u] + Adj[u][j].dis < distance[v]) {
                // 如果v未访问 且 以u为中介点可以使distance[v]更优
                distance[v] = distance[u] + Adj[u][j].dis; // 优化d[v]
            }
        }
    }
}
```

