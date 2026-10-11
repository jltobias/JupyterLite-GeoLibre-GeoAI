"""Small GeoJSON safeguards for the browser lessons (RFC 7946 §§3.1.9, 5).

These functions handle horizontal bboxes and small, non-polar convex rings
such as the H3 cells used in lab 05. They are not a general polygon overlay
engine: holes, pole-enclosing rings and arbitrarily large polygons need GIS
topology handling. See https://www.rfc-editor.org/rfc/rfc7946.html.
"""
import math


def horizontal_bbox(bbox):
    """Return west/south/east/north for 2D or 3D metadata; preserve missingness."""
    if bbox is None:
        return [None] * 4
    if len(bbox) not in (4, 6):
        raise ValueError("A STAC bbox must have four or six coordinates")
    half = len(bbox) // 2
    result = [bbox[0], bbox[1], bbox[half], bbox[half + 1]]
    if not all(isinstance(v, (float, int)) and math.isfinite(v) for v in result):
        raise ValueError("Horizontal bbox coordinates must be finite numbers")
    west, south, east, north = result
    if not (-180 <= west <= 180 and -180 <= east <= 180 and -90 <= south <= north <= 90):
        raise ValueError("Invalid longitude/latitude bounds")
    return result  # west > east is valid across the antimeridian


def _clip(points, bound, keep_greater):
    result = []
    previous = points[-1]
    inside = lambda p: p[0] >= bound if keep_greater else p[0] <= bound
    for current in points:
        if inside(previous) != inside(current):
            fraction = (bound - previous[0]) / (current[0] - previous[0])
            result.append([bound, previous[1] + fraction * (current[1] - previous[1])])
        if inside(current):
            result.append(list(current))
        previous = current
    return result


def split_antimeridian_ring(ring):
    """Cut a small convex lon/lat ring at ±180, returning GeoJSON geometry.

    Edges are linear in longitude/latitude, as GeoJSON specifies. No source
    values are changed; one cell remains one feature, possibly a MultiPolygon.
    Fail explicitly for a pole-enclosing ring instead of drawing a false band.
    """
    points = [list(p) for p in ring]
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    if len(points) < 3 or any(len(p) != 2 or not all(math.isfinite(v) for v in p)
                              or not (-180 <= p[0] <= 180 and -90 <= p[1] <= 90) for p in points):
        raise ValueError("Use at least three finite longitude/latitude vertices")
    unwrapped = [points[0]]
    for lon, lat in points[1:]:
        previous = unwrapped[-1][0]
        while lon - previous > 180:
            lon -= 360
        while lon - previous < -180:
            lon += 360
        unwrapped.append([lon, lat])
    if abs(unwrapped[-1][0] - unwrapped[0][0]) > 180:
        raise ValueError("Pole-enclosing cell: use a polar-aware GIS conversion before mapping")
    if max(p[0] for p in unwrapped) - min(p[0] for p in unwrapped) >= 180:
        raise ValueError("Use a small non-polar ring, not a hemisphere-scale polygon")
    polygons = []
    for shift in (-360, 0, 360):
        shifted = [[lon + shift, lat] for lon, lat in unwrapped]
        clipped = _clip(shifted, -180, True)
        if clipped:
            clipped = _clip(clipped, 180, False)
        if len(clipped) < 3:
            continue
        area2 = sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(clipped, clipped[1:]+clipped[:1]))
        if abs(area2) < 1e-12:
            continue
        if area2 < 0:
            clipped.reverse()
        polygons.append([clipped + [clipped[0]]])
    if not polygons:
        raise ValueError("Degenerate ring has no polygon area")
    if len(polygons) == 1:
        return {"type": "Polygon", "coordinates": polygons[0]}
    return {"type": "MultiPolygon", "coordinates": polygons}
