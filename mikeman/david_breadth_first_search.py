from enum import Enum
from dataclasses import dataclass

class SearchStatus(Enum):
    WAITING = 1,
    IN_PROGRESS = 2,
    COMPLETE_WITH_SOLUTION = 3,
    COMPLETE_NO_SOLUTION = 4

    def __str__(self):
        return str(self.name)


@dataclass
class StepResult:
    v: any
    neighbors_updated: any


class BreathFirstSearch:
    # Implements a generic BFS 
    # - Cells should provide a get_empty_neighbors() method
    # - Solution path is given from end_cell to start_cell
    #
    # Two operation modes:
    #
    # - STEPPED MODE
    #   - 1) call initalize_search()
    #   - 2) repeatedly invoke step() to explore each set of neighbors,
    #   - 3) finally get_solution() to retrieve the path
    #   - Note: step() returns a StepResult that can be used for visualization
    #
    # - SOLVE MODE
    #   - Only call solve() which will return a solution path or [] if no solution found


    def __init__(self):
        self.reset()

    def reset(self):
        self.start_cell = None
        self.end_cell = None
        self.parents = {}
        
        self.status = SearchStatus.WAITING

    def solve(self, start_cell, end_cell):
        self.initialize_search(start_cell, end_cell)
        while self.status == SearchStatus.IN_PROGRESS:
            self.step()
        if self.status == SearchStatus.COMPLETE_WITH_SOLUTION:
            return self.get_solution()
        else:
            return []

    def initialize_search(self, start_cell, end_cell):
        self.reset()
        
        self.start_cell = start_cell
        self.end_cell = end_cell

        self.need_visit = [self.start_cell]
        self.visited = [self.start_cell]

        self.status = SearchStatus.IN_PROGRESS

    def step(self):
        assert(self.status == SearchStatus.IN_PROGRESS)

        v = self.need_visit.pop() # pop back
        
        if v == self.end_cell:
            self.status = SearchStatus.COMPLETE_WITH_SOLUTION
            return StepResult(v,[])

        neighbors_to_visit = [n for n in v.get_empty_neighbors() if n not in self.visited]
        for neighbor in neighbors_to_visit:
            self.parents[neighbor] = v
            self.visited.append(neighbor)
            self.need_visit = [neighbor] + self.need_visit # push front

        if not self.need_visit:
            self.status = SearchStatus.COMPLETE_NO_SOLUTION
        else:
            self.status = SearchStatus.IN_PROGRESS
        return StepResult(v,neighbors_to_visit)

    def get_solution(self):
        assert(self.status == SearchStatus.COMPLETE_WITH_SOLUTION)

        v = self.end_cell
        solution_path = [v]
        while self.parents.get(v, None): # Start cell has no parent
            v = self.parents[v]
            solution_path.append(v)

        return list(reversed(solution_path))
