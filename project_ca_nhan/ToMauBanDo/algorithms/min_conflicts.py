import random
from algorithms.backtracking import build_adjacency_from_file

def map_color_constraint(var, value, neighbor, neighbor_value):
    return value != neighbor_value


def count_conflicts(var, value, assignment, neighbors, constraint):
    count = 0
    for neighbor in neighbors.get(var, []):
        if neighbor in assignment and not constraint(var, value, neighbor, assignment[neighbor]):
            count += 1
    return count


class MinConflictsSolver:
    def __init__(self, variables, domains, neighbors, constraint, fixed_colors=None):
        self.variables = list(variables)
        self.domains = {var: list(domains[var]) for var in self.variables}
        self.neighbors = neighbors
        self.constraint = constraint
        self.fixed_colors = fixed_colors or {}

    def initial_assignment(self):
        assignment = {}
        for var in self.variables:
            if var in self.fixed_colors:
                assignment[var] = self.fixed_colors[var]
            else:
                choices = self.domains[var]
                if not choices:
                    return None
                assignment[var] = random.choice(choices)
        return assignment

    def conflicted_vars(self, assignment):
        return [var for var in self.variables if var not in self.fixed_colors and count_conflicts(var, assignment[var], assignment, self.neighbors, self.constraint) > 0]

    def min_conflict_values(self, var, assignment):
        best = []
        best_score = None
        for value in self.domains[var]:
            score = count_conflicts(var, value, assignment, self.neighbors, self.constraint)
            if best_score is None or score < best_score:
                best_score = score
                best = [value]
            elif score == best_score:
                best.append(value)
        return best

    def solve(self, max_steps=10000):
        assignment = self.initial_assignment()
        if assignment is None:
            return None
        for _ in range(max_steps):
            conflicted = self.conflicted_vars(assignment)
            if not conflicted:
                return assignment
            var = random.choice(conflicted)
            values = self.min_conflict_values(var, assignment)
            if not values:
                return None
            assignment[var] = random.choice(values)
        if not self.conflicted_vars(assignment):
            return assignment
        return None

    def solve_steps(self, max_steps=10000):
        assignment = self.initial_assignment()
        if assignment is None:
            return
        yield {"action": "start", "assignment": dict(assignment)}
        for _ in range(max_steps):
            conflicted = self.conflicted_vars(assignment)
            if not conflicted:
                yield {"action": "goal", "assignment": dict(assignment)}
                return
            var = random.choice(conflicted)
            values = self.min_conflict_values(var, assignment)
            if not values:
                return
            assignment[var] = random.choice(values)
            yield {"action": "assign", "var": var, "value": assignment[var], "assignment": dict(assignment)}
        if not self.conflicted_vars(assignment):
            yield {"action": "goal", "assignment": dict(assignment)}


def create_map_coloring_csp(path, colors=None, fixed_colors=None, forbidden_colors=None):
    if colors is None:
        colors = ["red", "green", "blue", "yellow"]
    fixed_colors = fixed_colors or {}
    forbidden_colors = forbidden_colors or {}
    variables, neighbors = build_adjacency_from_file(path)
    domains = {}
    for var in variables:
        if var in fixed_colors:
            domains[var] = [fixed_colors[var]]
        else:
            domains[var] = [c for c in colors if c not in forbidden_colors.get(var, [])]
    return MinConflictsSolver(variables, domains, neighbors, map_color_constraint, fixed_colors=fixed_colors)


def solve_map_coloring(path, colors=None, fixed_colors=None, forbidden_colors=None, max_steps=10000):
    solver = create_map_coloring_csp(path, colors, fixed_colors, forbidden_colors)
    return solver.solve(max_steps=max_steps)


def solve_map_coloring_steps(path, colors=None, fixed_colors=None, forbidden_colors=None, max_steps=10000):
    solver = create_map_coloring_csp(path, colors, fixed_colors, forbidden_colors)
    yield from solver.solve_steps(max_steps=max_steps)
