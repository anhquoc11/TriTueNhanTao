import json
def build_adjacency_from_topojson(path):
    data = load_json_file(path)
    geometries = data.get("objects", {}).get("collection", {}).get("geometries", [])

    names = []
    polygons = []

    arcs = data.get("arcs", [])

    def decode_topojson_arc(arc_id, arcs_list):
        if arc_id < 0:
            arc_id = ~arc_id
            arc = list(reversed(arcs_list[arc_id]))
        else:
            arc = arcs_list[arc_id]
        return arc

    def extract_polygons_from_geometry(geometry):
        geom_type = geometry.get("type")
        arc_groups = geometry.get("arcs", [])
        if geom_type != "Polygon":
            return []
        rings = []
        for ring_arcs in arc_groups:
            points = []
            for arc_id in ring_arcs:
                arc = decode_topojson_arc(arc_id, arcs)
                if points and arc and points[-1] == arc[0]:
                    points.extend(arc[1:])
                else:
                    points.extend(arc)
            rings.append(points)
        return rings

    for g in geometries:
        name = g.get("properties", {}).get("name") or g.get("properties", {}).get("Tên")
        if not name:
            continue
        names.append(name)
        polys = extract_polygons_from_geometry(g)
        polygons.append(polys)

    neighbors = {name: set() for name in names}

    # build adjacency by shared edge segments
    def segments_from_polys(polys):
        segs = set()
        for ring in polys:
            for i in range(len(ring) - 1):
                a = (round(float(ring[i][0]), 6), round(float(ring[i][1]), 6))
                b = (round(float(ring[i+1][0]), 6), round(float(ring[i+1][1]), 6))
                if a <= b:
                    segs.add((a, b))
                else:
                    segs.add((b, a))
        return segs

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            segs_i = segments_from_polys(polygons[i])
            segs_j = segments_from_polys(polygons[j])
            if segs_i.intersection(segs_j):
                neighbors[names[i]].add(names[j])
                neighbors[names[j]].add(names[i])

    return names, neighbors
def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def share_border(poly1, poly2):
    # đơn giản hóa:
    # nếu có điểm chung hoặc giao nhau => coi là kề
    # poly can be GeoJSON geometry objects or lists of coordinates
    def segments_from_coords(coords):
        segs = set()
        # coords expected as list of linear rings: [ [ [x,y], ... ], ... ]
        for ring in coords:
            if not ring:
                continue
            for i in range(len(ring) - 1):
                a = (round(float(ring[i][0]), 6), round(float(ring[i][1]), 6))
                b = (round(float(ring[i+1][0]), 6), round(float(ring[i+1][1]), 6))
                # normalize segment direction
                if a <= b:
                    segs.add((a, b))
                else:
                    segs.add((b, a))
        return segs

    def extract_coords(geom):
        if isinstance(geom, dict):
            gtype = geom.get("type")
            coords = geom.get("coordinates", [])
            if gtype == "Polygon":
                return coords
            if gtype == "MultiPolygon":
                # flatten multipolygon as list of rings
                rings = []
                for poly in coords:
                    for ring in poly:
                        rings.append(ring)
                return rings
            return []
        # otherwise assume it's already a coordinates list
        return geom

    try:
        coords1 = extract_coords(poly1)
        coords2 = extract_coords(poly2)
    except Exception:
        return False

    segs1 = segments_from_coords(coords1)
    segs2 = segments_from_coords(coords2)

    # if any shared segment -> share border
    return len(segs1.intersection(segs2)) > 0
def build_adjacency_from_geojson(path):
    data = load_json_file(path)
    features = data["features"]

    names = []
    polygons = []

    for f in features:
        name = f["properties"].get("name") or f["properties"].get("Tên")
        if not name:
            continue

        names.append(name)
        polygons.append(f["geometry"])

    neighbors = {name: set() for name in names}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if share_border(polygons[i], polygons[j]):
                neighbors[names[i]].add(names[j])
                neighbors[names[j]].add(names[i])

    return names, neighbors
def build_adjacency_from_file(path):
    data = load_json_file(path)

    if data.get("type") == "Topology":
        return build_adjacency_from_topojson(path)

    if data.get("type") == "FeatureCollection":
        return build_adjacency_from_geojson(path)

    raise ValueError("Unknown format")

class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables
        self.domains = {var: list(domains[var]) for var in variables}
        self.neighbors = neighbors
        self.constraint = constraint
        self.curr_domains = None

        # thêm dòng này
        self.solution_found = False

    def assign(self, var, value, assignment):
        assignment[var] = value

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, value, assignment):
        count = 0
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment and not self.constraint(
                var,
                value,
                neighbor,
                assignment[neighbor]
            ):
                count += 1
        return count

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {
                var: list(self.domains[var])
                for var in self.variables
            }

    def suppose(self, var, value):
        self.support_pruning()

        removals = [
            (var, a)
            for a in self.curr_domains[var]
            if a != value
        ]

        self.curr_domains[var] = [value]

        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        removals.append((var, value))

    def restore(self, removals):
        for var, value in removals:
            self.curr_domains[var].append(value)

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def goal_test(self, assignment):
        return len(assignment) == len(self.variables)

    def select_unassigned_variable(self, assignment):

        unassigned = [
            v for v in self.variables
            if v not in assignment
        ]

        if not unassigned:
            return None

        # MRV + Degree
        return min(
            unassigned,
            key=lambda var:
            (
                len(self.choices(var)),
                -len(self.neighbors[var])
            )
        )

    def order_domain_values(self, var, assignment):

        if self.curr_domains:
            return list(self.curr_domains[var])

        return list(self.domains[var])

    def consistent(self, var, value, assignment):
        return self.nconflicts(
            var,
            value,
            assignment
        ) == 0

    def inference(
        self,
        var,
        value,
        assignment,
        removals
    ):
        self.support_pruning()

        for neighbor in self.neighbors.get(var, []):

            if neighbor not in assignment:

                for neighbor_value in list(
                    self.curr_domains[neighbor]
                ):

                    if not self.constraint(
                        var,
                        value,
                        neighbor,
                        neighbor_value
                    ):
                        self.prune(
                            neighbor,
                            neighbor_value,
                            removals
                        )

                if not self.curr_domains[neighbor]:
                    return False

        return True

    def backtracking_search(self):
        self.curr_domains = None
        return self.backtrack({})

    def backtracking_search_steps(self):
        self.curr_domains = None
        self.solution_found = False

        yield from self.backtrack_steps({})

    def backtrack(self, assignment):

        if self.goal_test(assignment):
            return assignment

        var = self.select_unassigned_variable(
            assignment
        )

        for value in self.order_domain_values(
            var,
            assignment
        ):

            if self.consistent(
                var,
                value,
                assignment
            ):

                self.assign(
                    var,
                    value,
                    assignment
                )

                removals = self.suppose(
                    var,
                    value
                )

                if self.inference(
                    var,
                    value,
                    assignment,
                    removals
                ):

                    result = self.backtrack(
                        assignment
                    )

                    if result is not None:
                        return result

                self.restore(removals)

                self.unassign(
                    var,
                    assignment
                )

        return None

    def backtrack_steps(self, assignment):

        if self.goal_test(assignment):

            self.solution_found = True

            yield {
                "action": "goal",
                "assignment": dict(assignment)
            }

            return

        var = self.select_unassigned_variable(
            assignment
        )

        for value in self.order_domain_values(
            var,
            assignment
        ):

            if self.consistent(
                var,
                value,
                assignment
            ):

                self.assign(
                    var,
                    value,
                    assignment
                )

                yield {
                    "action": "assign",
                    "var": var,
                    "value": value,
                    "assignment": dict(assignment)
                }

                removals = self.suppose(
                    var,
                    value
                )

                if self.inference(
                    var,
                    value,
                    assignment,
                    removals
                ):

                    yield from self.backtrack_steps(
                        assignment
                    )

                    if self.solution_found:
                        return

                self.restore(removals)

                self.unassign(
                    var,
                    assignment
                )

                yield {
                    "action": "remove",
                    "var": var,
                    "value": value,
                    "assignment": dict(assignment)
                }

        return
def map_color_constraint(var, value, neighbor, neighbor_value):
    return value != neighbor_value
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
            domain = [c for c in colors if c not in forbidden_colors.get(var, [])]
            domains[var] = domain

    return CSP(
        variables,
        domains,
        neighbors,
        map_color_constraint
        )
def solve_map_coloring(path, colors=None, fixed_colors=None, forbidden_colors=None):
    csp = create_map_coloring_csp(path, colors, fixed_colors, forbidden_colors)
    return csp.backtracking_search()
def solve_map_coloring_steps(path, colors=None, fixed_colors=None, forbidden_colors=None):
    csp = create_map_coloring_csp(path, colors, fixed_colors, forbidden_colors)
    yield from csp.backtracking_search_steps()