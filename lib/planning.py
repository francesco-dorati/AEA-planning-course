import numpy as np
from enum import Enum
from queue import PriorityQueue

def astar_grid(grid, start, goal):
    """Find shortest path from start to end with A* algorithm

    Args:
        grid (matrix): space grid with obstacles
        start (tuple): start position
        goal (tuple): goal position
        
    Returns:
        list of tuples: list of all visited points
    """
    
    class Action(Enum):
        # (i, j, cost)
        LEFT = (0, -1, 1)
        RIGHT = (0, 1, 1)
        UP = (-1, 0, 1)
        DOWN = (1, 0, 1)
        UR_DIAG = (-1, 1, 1.41)
        UL_DIAG = (-1, -1, 1.41)
        DR_DIAG = (1, 1, 1.41)
        DL_DIAG = (1, -1, 1.41)

        def __str__(self):
            if self == self.LEFT:
                return '<'
            elif self == self.RIGHT:
                return '>'
            elif self == self.UP:
                return '^'
            elif self == self.DOWN:
                return 'v'
            elif self == self.UR_DIAG:
                return '/^'
            elif self == self.UL_DIAG:
                return '\\^'
            elif self == self.DR_DIAG:
                return '\\v'
            elif self == self.DL_DIAG:
                return '/v'

        @property
        def cost(self):
            return self.value[2]
        
        @property
        def delta(self):
            return (self.value[0], self.value[1])
    
    def valid_moves(current):
        valid = []
        for act in Action:
            delta = act.value
            next_pos = (current[0] + delta[0], current[1] + delta[1])

            is_inside_grid = (next_pos[0] >= 0 and next_pos[0] < len(grid)) and (next_pos[1] >= 0 and next_pos[1] < len(grid[0])) 
            
            if is_inside_grid and grid[next_pos] != 1:
                valid.append(act)
            
        return valid

    def dist(pos, goal):
        return np.sqrt(abs(goal[0]-pos[0])**2 + abs(goal[1]-pos[1])**2)
    
    q = PriorityQueue()     # points to value (dist+price, dist, price, coord)
    q.put((dist(start, goal), 0, start))

    visited = set()         # visited points
    visited.add(start)

    branch = {}             # history of path

    count = 0               # count computations

    while True:
        curr = q.get()
        cost = curr[1]
        pos = curr[2]

        if pos == goal:
            break

        for action in valid_moves(pos):
            count += 1
            
            new_pos = (pos[0] + action.delta[0], pos[1] + action.delta[1])
            new_dist = dist(new_pos, goal)
            new_cost = cost + action.cost

            if new_pos not in visited:
                visited.add(new_pos)
                q.put((new_dist+new_cost, new_cost, new_pos))
                branch[new_pos] = (pos, action, new_cost)
        
            elif new_pos in branch and branch[new_pos][2] > new_cost:
                branch[new_pos] = (pos, action, new_cost)


    # traverse back
    path = []
    curr = goal

    while branch[curr][0] != start:
        # append each new node to the path
        path.append(branch[curr][0])
        curr = branch[curr][0]
        
    path = path[::-1]

    return path, branch[goal][2]


def astar_graph(edges, start, goal):
    # start and goal are nodes

    def dist(p1, p2):
        return np.sqrt(abs(p2[0]-p1[0])**2 + abs(p2[1]-p1[1])**2)
    
    def connected_nodes(curr):
        nodes = []
        for e in edges:
            if e[0] == curr:
                nodes.append(e[1])
            elif e[1] == curr:
                nodes.append(e[0])
        return nodes
    
    q = PriorityQueue()
    q.put((dist(start, goal), 0, start))

    visited = set()
    visited.add(start)

    branch = {}

    found = False

    while True:
        curr = q.get()
        cost = curr[1]
        pos = curr[2]

        if pos == goal:
            found = True
            break
        
        if q.empty():
            break
        
        if not connected_nodes(pos):
            continue
        

        for next_node in connected_nodes(pos):
            traversing_cost = dist(curr, next_node)
            new_cost = traversing_cost + cost
            new_dist = dist(next_node, goal)

            if next_node not in visited:
                q.put((new_dist + new_cost, new_cost, next_node))
                visited.add(next_node)
                branch[next_node] = (pos, new_cost)

            elif next_node in branch and branch[next_node][1] > new_cost:
                branch[next_node] = (pos, new_cost)

    if found:
        path = []
        c = goal
        while c != start:
            path.append(c)
            c = branch[c][0]
        path.append(start)
        path = path[::-1]
        return path

