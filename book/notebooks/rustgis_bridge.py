"""Small, local GeoJSON/GeoAI bridge; no RustGIS Python dependency or network calls.

All locations are invented teaching points, not health facilities or patients.
GeoJSON stores longitude first. The haversine model receives latitude first.
"""
from collections import Counter
from copy import deepcopy
import json
import math
from pathlib import Path
from urllib.parse import urlencode

EARTH_RADIUS_M = 6_371_008.8
PUBLIC_DATA = "https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/files/data/rustgis-groups.geojson"


def sample_sites():
    """Two invented nine-point grids plus two isolated points near London."""
    coordinates = [(round(lon + dx * .003, 6), round(lat + dy * .002, 6))
                   for lon, lat in [(-.14, 51.50), (-.08, 51.51)]
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    coordinates += [(-.20, 51.53), (-.02, 51.48)]
    return {"type": "FeatureCollection", "features": [
        {"type": "Feature", "id": f"demo-{i:02d}",
         "geometry": {"type": "Point", "coordinates": list(xy)},
         "properties": {"name": f"Invented site {i:02d}", "synthetic": True}}
        for i, xy in enumerate(coordinates, 1)]}


def validate_sites(collection):
    """Check this lesson's point schema before modeling/exporting, not all GeoJSON."""
    if collection.get("type") != "FeatureCollection" or not collection.get("features"):
        raise ValueError("Expected a nonempty GeoJSON FeatureCollection")
    ids = set()
    for feature in collection["features"]:
        geometry = feature.get("geometry", {})
        xy = geometry.get("coordinates", [])
        if (feature.get("type") != "Feature" or geometry.get("type") != "Point"
                or len(xy) != 2 or any(type(v) not in (int, float) or not math.isfinite(v) for v in xy)
                or not (-180 <= xy[0] <= 180 and -90 <= xy[1] <= 90)):
            raise ValueError("Expected finite WGS84 Point [longitude, latitude] coordinates")
        identifier = feature.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in ids:
            raise ValueError("Each point needs a unique string id")
        ids.add(identifier)
        if not isinstance(feature.get("properties"), dict):
            raise ValueError("Each point needs properties")
    json.dumps(collection, allow_nan=False)
    return collection


def fit_groups(sites, radius_m=350):
    """Unweighted DBSCAN: no clinical attributes, risk scores or learned forecast."""
    import numpy as np
    from sklearn.cluster import DBSCAN
    validate_sites(sites)
    if type(radius_m) not in (int, float) or not math.isfinite(radius_m) or radius_m <= 0:
        raise ValueError("radius_m must be finite and positive")
    # Reverse GeoJSON [lon, lat] into haversine [lat, lon], then convert to radians.
    lat_lon = np.radians([f["geometry"]["coordinates"][::-1] for f in sites["features"]])
    labels = DBSCAN(eps=radius_m / EARTH_RADIUS_M, min_samples=3,
                    metric="haversine", algorithm="brute").fit_predict(lat_lon)
    result = deepcopy(sites)
    for feature, label in zip(result["features"], labels):
        feature["properties"].update(group=int(label), neighbor_radius_m=radius_m,
                                     method="DBSCAN; haversine; min_samples=3")
    return validate_sites(result)


def group_counts(grouped):
    return dict(sorted(Counter(f["properties"]["group"] for f in grouped["features"]).items()))


def plot_sites(sites, title):
    import matplotlib.pyplot as plt
    validate_sites(sites)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    grouped = "group" in sites["features"][0]["properties"]
    labels = sorted({f["properties"].get("group", 0) for f in sites["features"]})
    for label in labels:
        points = [f["geometry"]["coordinates"] for f in sites["features"]
                  if f["properties"].get("group", 0) == label]
        color = "#64748b" if label == -1 else plt.get_cmap("tab10")(label % 10)
        caption = ("Unassigned (-1)" if label == -1 else f"Group {label}") if grouped else "Invented sites"
        ax.scatter(*zip(*points), s=55, color=color, label=caption)
    ax.set(xlabel="Longitude (degrees)", ylabel="Latitude (degrees)", title=title,
           xlim=(-.215, -.005), ylim=(51.47, 51.54))
    ax.set_aspect(1 / math.cos(math.radians(51.5)))
    ax.grid(alpha=.2)
    ax.legend(loc="upper right")
    fig.tight_layout()
    return fig


def export_groups(grouped, directory="exports"):
    """Save GeoJSON and a separate provenance card in the notebook filesystem."""
    validate_sites(grouped)
    radii = {f["properties"]["neighbor_radius_m"] for f in grouped["features"]}
    if len(radii) != 1:
        raise ValueError("Export one model setting at a time")
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    data_path = target / "my-rustgis-groups.geojson"
    data_path.write_text(json.dumps(grouped, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    card = {"dataset": "Invented teaching points; not health facilities or patient records",
            "source": "JupyterLite-GeoLibre-GeoAI notebook 22 / sample_sites()",
            "data_origin": "Repository-authored synthetic example; no third-party source dataset",
            "coordinate_order": "WGS84 longitude, latitude in degrees",
            "method": "DBSCAN; haversine; min_samples=3; unweighted locations",
            "neighbor_radius_m": next(iter(radii)), "group_counts": group_counts(grouped),
            "limits": "Groups are location patterns, not risk, causes, travel times or recommendations"}
    card_path = target / "my-rustgis-groups-provenance.json"
    card_path.write_text(json.dumps(card, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data_path, card_path


def public_view_url(globe=False):
    """Launch the published 350 m example, never an unsaved notebook result."""
    params = {"data": PUBLIC_DATA}
    if globe:
        params["projection"] = "globe"
    return "https://web.rustgis.app/?blank&" + urlencode(params)
