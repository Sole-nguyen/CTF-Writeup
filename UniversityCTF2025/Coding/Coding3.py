def count_neighbors(grid, i, j):
    """Count alive neighbors for cell at position (i, j)"""
    n = len(grid)
    count = 0
    # Check all 8 surrounding cells
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                count += grid[ni][nj]
    return count

def parse_rule(rulestring):
    """Parse rulestring like 'B25/S05' into birth and survival sets"""
    parts = rulestring.split('/')
    birth_part = parts[0][1:]  # Remove 'B'
    survival_part = parts[1][1:]  # Remove 'S'
    
    birth = set(int(d) for d in birth_part if d.isdigit())
    survival = set(int(d) for d in survival_part if d.isdigit())
    
    return birth, survival

def simulate_generation(grid, birth, survival):
    """Simulate one generation of the cellular automaton"""
    n = len(grid)
    new_grid = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            neighbors = count_neighbors(grid, i, j)
            
            if grid[i][j] == 1:  # alive cell
                if neighbors in survival:
                    new_grid[i][j] = 1
            else:  # dead cell
                if neighbors in birth:
                    new_grid[i][j] = 1
    
    return new_grid

# Read input
n = int(input())
grid = []
for _ in range(n):
    line = input().strip()
    grid.append([int(c) for c in line])

rulestring = input().strip()
t = int(input())

# Parse rule
birth, survival = parse_rule(rulestring)

# Simulate T generations
for _ in range(t):
    grid = simulate_generation(grid, birth, survival)

# Output final grid
for row in grid:
    print(''.join(str(c) for c in row))
