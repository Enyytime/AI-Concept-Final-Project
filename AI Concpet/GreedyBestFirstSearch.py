from queue import PriorityQueue

v = 14
graph = [[] for _ in range(v)]

# Heuristic function (example)
# This function should return an estimated distance from node to target.
def heuristic(node, target):
    h = [17, 10, 13, 4, 4, 2, 1, 0]  # Example heuristic values (you can adjust them)
    return h[node]

# Function to implement Greedy Best First Search with Heuristic
def best_first_search_with_heuristic(actual_Src, target, n):
    visited = [False] * n
    parent = [-1] * n  # To keep track of the path
    pq = PriorityQueue()
    pq.put((heuristic(actual_Src, target), actual_Src))  # Use heuristic to prioritixze
    visited[actual_Src] = True
    while not pq.empty():
        u = pq.get()[1]

        if u == target:
            break

        for v, c in graph[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u  # Store the path
                pq.put((heuristic(v, target), v))  # Use heuristic for priority

    # Reconstruct the path from source to target
    path = []
    crawl = target
    while parent[crawl] != -1:
        path.append(crawl)
        crawl = parent[crawl]
    path.append(actual_Src)

    print("Path:", path[::-1])

# Function for adding edges to the graph
def addedge(x, y, cost):
    graph[x].append((y, cost))
    graph[y].append((x, cost))

# Add edges to the graph
addedge(0, 1, 6)
addedge(0, 2, 5)
addedge(0, 3, 10)
addedge(1, 4, 6)
addedge(2, 4, 6)
addedge(2, 5, 7)
addedge(3, 5, 6)
addedge(4, 6, 4)
addedge(5, 6, 6)
addedge(6, 7, 3)

# Define the source and target
source = 0
target = 7

# Perform Best First Search with Heuristic
best_first_search_with_heuristic(source, target, v)
