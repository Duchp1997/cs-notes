# DFS(深度优先搜索)

## 递归算法

获取全排列：

```C++
#include <iostream>
#include <vector>
using namespace std;

int n;

template <typename T>
struct ValueNode {
    T value;
    bool isSelected;
};

typedef ValueNode<int> Num;

void DFS(vector<Num> & nums, vector<int> & select, int index) {
    if(index == n) {
        for(auto num : select)
            cout << num << ' ';
        cout << endl;
        return;
    }

    for(int i = 0; i < n; i++) {
        if(nums[i].isSelected == false) {
            nums[i].isSelected = true;
            select.push_back(nums[i].value);
            DFS(nums, select, index + 1);
            select.pop_back();
            nums[i].isSelected = false;
        }
    }
}

int main() {

    while(cin >> n) {
        vector<Num> nums = vector<Num>();
        for(int i = 1; i <= n; i++) {
            Num num;
            num.isSelected = false;
            num.value = i;
            nums.push_back(num);
        }

        vector<int> select = {};
        DFS(nums, select, 0);
    }

    return 0;
}
```

