def make_set(n):
    # initializing a disjoint set union dictionary where each node is the parent of itself
    dsu={}
    for i in range(n): 
        dsu[i]=i
    return dsu

def find(parent, i):
    # Base case: If the parent of i is i itself, then i is the root element
    if parent[i] == i:
        return i
    # Recursive case: Follow the parent pointer to find the root element
    return find(parent, parent[i])

def union(parent, i, j):
    # Find the root elements of i and j
    root_i = find(parent, i)
    root_j = find(parent, j)
    # Union the sets represented by i and j
    if root_i!=root_j:
        parent[root_j] = root_i














