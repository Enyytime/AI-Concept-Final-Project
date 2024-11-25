from queue import PriorityQueue

# Graph definition
v = 14
graph = [[] for _ in range(v)]

# Heuristic values (assuming we want to reach node 9 as target)
# This is just an example heuristic; you can adjust these values as needed
heuristic = [17, 10, 13, 4, 4, 2, 1, 0]
# Function to add edges to the graph
def addedge(x, y, cost):
    graph[x].append((y, cost))
    graph[y].append((x, cost))

# Adding edges
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
# A* Search Algorithm
def a_star_search(start, target):
    pq = PriorityQueue()  # Priority queue to hold nodes with their cost (f = g + h)
    pq.put((0 + heuristic[start], 0, start))  # f = g + h, g = 0 for start node

    visited = [False] * v
    parent = [-1] * v  # To store the path
    g_cost = [float('inf')] * v  # Cost from start to each node
    g_cost[start] = 0

    while not pq.empty():
        f, g, current = pq.get()

        if current == target:
            # Reconstruct the path
            path = []
            while current != -1:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Return reversed path (from start to target)

        visited[current] = True

        for neighbor, cost in graph[current]:
            new_g = g + cost
            new_f = new_g + heuristic[neighbor]

            if not visited[neighbor] and new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                parent[neighbor] = current
                pq.put((new_f, new_g, neighbor))

    return None  # If no path is found

# Define the source and target
source = 0
target = 7

# Run A* search
path = a_star_search(source, target)
print("Path found:", path)
