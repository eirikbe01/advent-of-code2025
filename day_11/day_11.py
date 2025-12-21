
file = open("input.txt").readlines()
file = [line.strip() for line in file]

def dfs(src: str, dest: str, graph: dict, current_path: list[str], all_paths: list[list[str]]):

    current_path.append(src)

    if src == dest:
        all_paths.append(current_path.copy())
    else:
        for neighbor in graph[src]:
            dfs(neighbor, dest, graph, current_path, all_paths)

    current_path.pop()


def find_paths(file: list[str], src: str, dest: str):
    graph = dict()
    for line in file:
        line = line.split(" ")
        node, neighbors = line[0].strip(":"), line[1:]
        if not node in graph.keys():
            graph[node] = neighbors
    
    all_paths = []
    path = []

    dfs(src, dest, graph, path, all_paths)

    return all_paths


paths = find_paths(file, "you", "out")

for path in paths:
    print(path)

print(f"Number of different paths: {len(paths)}")