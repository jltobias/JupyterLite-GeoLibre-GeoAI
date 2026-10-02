"""Small, browser-compatible visual and synthetic-data helpers for the labs.

No network calls, credentials, model calls, or native GIS dependency on import.
Every generated geography is a teaching fixture, not an observed dataset.
"""

import base64
import html
import io
import json
import math
from pathlib import Path


COLORS = ["#2563eb", "#d97706", "#0f766e", "#9333ea", "#dc2626", "#475569"]


def style_plots():
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.figsize": (10, 4), "figure.dpi": 110,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "axes.titlepad": 12,
        "axes.labelcolor": "#334155", "text.color": "#0f172a",
        "axes.prop_cycle": plt.cycler(color=COLORS),
        "savefig.bbox": "tight",
    })


def local_lonlat(x_m, y_m, origin=(-122.3, 37.9)):
    """Teaching approximation for a small (<10 km) local patch, not a GIS CRS."""
    return [origin[0] + float(x_m) / (111320 * math.cos(math.radians(origin[1]))),
            origin[1] + float(y_m) / 111320]


def grid_features(values, *, field="value", cell_m=200, origin=(-122.3, 37.9)):
    """Map a south-to-north array onto closed GeoJSON polygons (lon, lat)."""
    import numpy as np
    values = np.asarray(values, dtype=float)
    if values.ndim != 2 or not np.isfinite(values).all() or cell_m <= 0:
        raise ValueError("Use a finite 2D array and positive cell_m")
    features = []
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            corners = [(col, row), (col + 1, row), (col + 1, row + 1),
                       (col, row + 1), (col, row)]
            ring = [local_lonlat(x * cell_m, y * cell_m, origin) for x, y in corners]
            features.append({"type": "Feature", "properties": {
                "id": f"r{row:02d}c{col:02d}", field: float(values[row, col]),
                "source": "synthetic teaching fixture",
            }, "geometry": {"type": "Polygon", "coordinates": [ring]}})
    return {"type": "FeatureCollection", "features": features}


def teaching_city(n=8):
    """Deterministic district grid: heat, canopy and population are invented."""
    import numpy as np
    import pandas as pd
    r, c = np.mgrid[:n, :n]
    canopy = 15 + 45 * (1 + np.sin(c * .7) * np.cos(r * .6)) / 2
    heat = 27 + 9 * np.exp(-((c - 5) ** 2 + (r - 3) ** 2) / 9) - canopy / 30
    population = (80 + 250 * (1 + np.sin(r + c / 3))).astype(int)
    fc = grid_features(heat, field="temperature_c")
    for i, f in enumerate(fc["features"]):
        f["properties"].update(canopy_pct=float(canopy.flat[i]),
                               population=int(population.flat[i]))
    return pd.DataFrame([f["properties"] for f in fc["features"]]), fc


def plotly_view(figure, *, height=520):
    """Isolate Plotly JS in an iframe; works without a Plotly widget extension.

    Needs the Plotly CDN for interactive rendering. Pair it with a saved static
    figure in the book. It neither fetches data nor exposes kernel state.
    """
    from IPython.display import HTML
    page = figure.to_html(include_plotlyjs="cdn", full_html=True,
                          config={"responsive": True, "displaylogo": False})
    return HTML(f'<iframe title="Interactive chart: drag to rotate, scroll to zoom" '
                f'sandbox="allow-scripts" style="width:100%;height:{int(height)}px;border:0" '
                f'srcdoc="{html.escape(page, quote=True)}"></iframe>')


def figure_data_url(figure):
    """Encode a labeled matplotlib evidence figure for an Astra image request."""
    buf = io.BytesIO()
    figure.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def save_json(path, value):
    """Save finite JSON in the notebook filesystem, downloadable in Lite."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")
    return str(path)
