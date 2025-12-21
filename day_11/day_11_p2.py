
file = open("input.txt").readlines()
file = [line.strip() for line in file]

def dfs(src: str, dest: str, graph: dict, memo: dict, seen_fft: bool, seen_dac: bool) -> int:
    key = (src, seen_fft, seen_dac)
    if key in memo:
        return memo[key]
    
    if src == dest:
        return 1 if (seen_fft and seen_dac) else 0
    
    total = 0
    for neighbor in graph[src]:
        total += dfs(neighbor, dest, graph, memo, 
                     seen_fft or (neighbor == "fft"), 
                     seen_dac or (neighbor == "dac"))
    memo[key] = total
    return total


def find_paths(file: list[str], src: str, dest: str):
    graph: dict[str, list[str]] = dict()
    for line in file:
        line = line.split(" ")
        node, neighbors = line[0].strip(":"), line[1:]
        graph[node] = neighbors
    
        for neighbor in neighbors:
            if neighbor not in graph:
                graph[neighbor] = graph.get(neighbor, [])
    
    memo = {}
    return dfs(
        src, dest, graph, 
        memo=memo, 
        seen_fft=(src == "fft"),
        seen_dac=(src == "dac"),
    )

count = find_paths(file, "svr", "out")

print(f"Number of different paths: {count}")