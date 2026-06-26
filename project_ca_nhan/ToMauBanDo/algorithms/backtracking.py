import json
from pathlib import Path


def load_json_file(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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
        polygons.append(extract_polygons_from_geometry(g))

    neighbors = {name: set() for name in names}

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
            if segments_from_polys(polygons[i]).intersection(segments_from_polys(polygons[j])):
                neighbors[names[i]].add(names[j])
                neighbors[names[j]].add(names[i])

    return names, neighbors


def share_border(poly1, poly2):
    def segments_from_coords(coords):
        segs = set()
        for ring in coords:
            if not ring:
                continue
            for i in range(len(ring) - 1):
                a = (round(float(ring[i][0]), 6), round(float(ring[i][1]), 6))
                b = (round(float(ring[i+1][0]), 6), round(float(ring[i+1][1]), 6))
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
                rings = []
                for poly in coords:
                    for ring in poly:
                        rings.append(ring)
                return rings
            return []
        return geom

    try:
        coords1 = extract_coords(poly1)
        coords2 = extract_coords(poly2)
    except Exception:
        return False

    segs1 = segments_from_coords(coords1)
    segs2 = segments_from_coords(coords2)
    return len(segs1.intersection(segs2)) > 0


def build_adjacency_from_geojson(path):
    data = load_json_file(path)
    features = data.get("features", [])

    names = []
    polygons = []

    for f in features:
        properties = f.get("properties", {})
        name = properties.get("name") or properties.get("Tên")
        if not name:
            continue
        names.append(name)
        polygons.append(f.get("geometry"))

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


class MapColoringCSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = list(variables)
        self.domains = {var: list(domains[var]) for var in self.variables}
        self.neighbors = neighbors
        self.constraint = constraint

    def assign(self, var, value, assignment):
        assignment[var] = value

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def consistent(self, var, value, assignment):
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment and not self.constraint(var, value, neighbor, assignment[neighbor]):
                return False
        return True

    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var
        return None

    def order_domain_values(self, var, assignment):
        return list(self.domains[var])

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return dict(assignment)

        var = self.select_unassigned_variable(assignment)
        if var is None:
            return None

        for value in self.order_domain_values(var, assignment):
            if self.consistent(var, value, assignment):
                self.assign(var, value, assignment)
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                self.unassign(var, assignment)
        return None

    def backtrack_steps(self, assignment):
        if len(assignment) == len(self.variables):
            yield {"action": "goal", "assignment": dict(assignment)}
            return

        var = self.select_unassigned_variable(assignment)
        if var is None:
            return

        for value in self.order_domain_values(var, assignment):
            if self.consistent(var, value, assignment):
                self.assign(var, value, assignment)
                yield {"action": "assign", "var": var, "value": value, "assignment": dict(assignment)}
                for step in self.backtrack_steps(assignment):
                    yield step
                    if step.get("action") == "goal":
                        return
                self.unassign(var, assignment)
                yield {"action": "remove", "var": var, "value": value, "assignment": dict(assignment)}
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
            domains[var] = [c for c in colors if c not in forbidden_colors.get(var, [])]

    return MapColoringCSP(variables, domains, neighbors, map_color_constraint)


def solve_map_coloring(path, colors=None, fixed_colors=None, forbidden_colors=None):
    csp = create_map_coloring_csp(path, colors, fixed_colors, forbidden_colors)
    return csp.backtrack({})


def solve_map_coloring_steps(path, colors=None, fixed_colors=None, forbidden_colors=None):
    csp = create_map_coloring_csp(path, colors, fixed_colors, forbidden_colors)
    yield from csp.backtrack_steps({})


def verify_solution(solution, neighbors):
    """Kiểm tra xem lời giải có hợp lệ không (các vùng kề nhau phải khác màu)"""
    if not solution:
        return True, []
    
    invalid_pairs = []
    for region, color in solution.items():
        for neighbor in neighbors.get(region, []):
            if neighbor in solution and solution[neighbor] == color:
                invalid_pairs.append((region, neighbor, color))
    
    return len(invalid_pairs) == 0, invalid_pairs
