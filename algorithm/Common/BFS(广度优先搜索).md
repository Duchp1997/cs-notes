# BFS(广度优先搜索)

## 基本模版

```C++
void BFS(int s) { // s为第一个节点
	queue(int) q;
	q.push(s);
  	while(!q.empty()) {
    	取出队首元素top;
      	访问队首元素top;
      	队首元素top出队;
      	将top的下一层节点中未入队的节点入队,标记为已入队
  	}
}
```

