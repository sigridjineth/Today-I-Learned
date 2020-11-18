# 신장 트리 Spinning Tree
### 정의
* 하나의 그래프가 있을 때 모든 노드를 포함하면서 사이클이 존재하지 않는 부분 그래프
* 트리의 성립 조건은 모든 노드가 포함되어 서로 연결되며 사이클이 존재하지 않는 것이다.

![](https://i.imgur.com/UkEO6OM.png)

## 크루스칼 알고리즘 Kruskal's Algorithm
### 정의
* 최소한의 비용으로 신장 트리를 찾을 때 사용하는 알고리즘이다.
* N개의 도시가 존재하는 상황에서 두 도시 사이에 도로를 놓아 전체 도시를 연결시킬 수 있도록 도로를 놓는다고 생각해보자.
    * 2개의 도시 A, B가 있다. A에서 B로 연결되는 통로가 반드시 존재하도록 도로를 설치하자. 최소한의 비용으로 연결하여라.
        ![](https://i.imgur.com/epqmLFW.png)
    * 당연히 23 + 13 = 36이 최소 비용이다.

### 알고리즘
* 가. 간선 데이터를 비용에 따라 오름차순 처리한다.
* 나. 간선을 하나씩 확인하며 현재의 간선이 싸이클을 발생시키는 지 확인한다.
    * 싸이클이 발생하면, 최소 신장 트리에 포함시킨다.
    * 싸이클이 발생하지 않으면, 최소 신장 트리에 포함시키지 않는다.
* 최소 신장 트리는 트리 구조이므로, 신장 트리에 포함되는 간선의 개수는 노드의 개수에서 1을 제외한 것과 마찬가지다.

### 예시
![](https://i.imgur.com/kchMV45.png)
* Step 0. 
    * 간선 정보만 빼내어 간선의 첫 번째 원소 순으로 정렬해보자.
    * (1, 2, 29), (1, 5, 75), (2, 3, 35), (2, 6, 34), (3, 4, 7), (4, 6, 23), (4, 7, 13), (5, 6, 53), (6, 7, 25)
    * 여기서 (노드A, 노드B, 간선비용) 으로 해석할 것!!
* Step 1. 
    * 가장 짧은 간선을 선택한다. (3, 4)가 선택되고, 집합에 포함한다. 3과 4에 대하여 union 함수를 수행하여 동일한 집합에 속하도록 한다.
* Step 2. 
    * 다음으로 비용이 적은 (4, 7)을 선택한다. 4와 7은 같은 집합에 속해있지 않으므로, 4와 7에 대하여 union 함수를 호출한다.
* Step 3. 
    * (4, 6)을 선택한다. 4와 6은 같은 집합에 속해있지 않으므로, 4와 6에 대하여 union 함수를 호출한다.
* Step 4. 
    * (6, 7)을 선택한다. 노드 6과 7은 동일한 루트 노드를 포함한다. 따라서 union 함수를 호출하지 않는다. 이미 같은 집합에 속해있기 때문이다.
* Step 5. 
    * (1, 2)을 선택한다. 1과 2는 같은 집합이 아니므로 union 함수를 호출한다.
* Step 6. 
    * (2, 6)을 선택한다. 역시 같은 집합이 아니므로 union 함수를 호출한다.
* Step 7. 
    * (2, 3)을 선택한다. 2와 3은 이미 이들의 루트가 동일한 집합에 속해있으므로 호출하지 않는다.
* Step 8. 
    * (5, 6)을 선택한다. 같은 집합에 없으므로 호출한다.
* Step 9. 
    * (1, 5)를 선택한다. 1과 5의 루트가 동일한 집합에 있으므로 호출하지 않는다.

#### 결론

![](https://i.imgur.com/9pXD6ZI.png)

### 코드
```javascript
kruskal = () => {
    [v, e] = window.prompt().split(" ").map((element) => Number(element));
    let parent = new Array(v+1).fill(0);
    edges = [];
    result = 0;
    for (let i = 1; i < v+1; i++) {
        parent[i] = i;
    };
    for (let i = 0; i < e; i++) {
        [a, b, cost] = window.prompt().split(" ").map((element) => Number(element));
        edges.push({
            cost: cost,
            a: a,
            b: b
        }); // 비용 순으로 정렬하기 위하여 비용을 첫 번째 원소로 설정
    };

    sort(edges, 0, edges.length-1);

    for (let edge of edges) {
        cost = edge.cost;
        a = edge.a;
        b = edge.b;
        // 싸이클이 발생하지 않는 경우에만 집합을 포함
        if (find_parent(parent,a) != find_parent(parent, b)) {
            union_parent(parent, a, b);
            result = result + cost;
        };
    };

    return result;
};

// 퀵 소트를 이용하여 정렬하였다.
sort = (array, start, end) => {
    // 원소가 1개일 때는 종료한다.
    if (start >= end) {
        return;
    };
    // 피벗은 첫 번째 원소이다.
    let pivot = start;
    let left = start + 1;
    let right = end;
    // 1단계를 수행한다.
    while (left <= right) {
        // 피벗보다 더 큰 데이터를 찾을 때까지 반복한다.
        while ((left <= end) && (array[left] < array[pivot])) {
            left = left + 1;
        };
        // 피벗보다 더 작은 데이터를 찾을 때까지 반복한다.
        while ((right > start) && (array[right] >= array[pivot])) {
            right = right - 1;
        };
        // 만약 엇갈렸다면, 작은 데이터와 피벗을 서로 교체한다. Divide(분할)
        if (left > right) {
            let tempSmallData = array[right];
            array[right] = array[pivot];
            array[pivot] = tempSmallData;
        } else { // 엇갈리지 않았다면 작은 데이터와 큰 데이터를 교체
            let tempBigData = array[left];
            array[left] = array[right];
            array[right] = tempBigData;
        }
    };
    sort(array, start, right - 1);
    sort(array, right + 1, end);
};
```
