"""Small historical-data lesson: geographic clustering, not causal inference.

No HTTP requests, generated code, patient data, or synthetic replacements.
The sklearn estimator receives only latitude/longitude, never pumps or deaths.
"""
from pathlib import Path
import math

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

EARTH_RADIUS_M = 6_371_008.8
RADII = (25, 50, 100)
COLORS = ('#6b46c1', '#087f8c', '#c05621', '#2563eb', '#a42672', '#4d7c0f',
          '#75512b', '#005f73', '#b91c1c', '#4f46e5', '#087f5b', '#7c3a8d')
UNASSIGNED = '#71717a'
DATA = Path(__file__).resolve().parent / 'data/cholera'


def coordinates(frame):
    """sklearn haversine uses [latitude, longitude] in radians, not GeoJSON order."""
    values = frame[['LAT', 'LON']].to_numpy(dtype=float)
    if not len(values) or not np.isfinite(values).all():
        raise ValueError('Locations must be nonempty and have finite coordinates.')
    if (np.abs(values[:, 0]) > 90).any() or (np.abs(values[:, 1]) > 180).any():
        raise ValueError('Latitude/longitude outside their valid ranges.')
    return np.radians(values)


def load_records(directory=DATA):
    """Read the bundled tables; a missing or invalid file is an explicit error."""
    directory = Path(directory)
    deaths = pd.read_csv(directory / 'cholera_deaths.csv')
    pumps = pd.read_csv(directory / 'pumps.csv')
    for frame in (deaths, pumps):
        coordinates(frame)
        if frame.FID.isna().any() or frame.FID.duplicated().any():
            raise ValueError('Each source record must have a unique FID.')
    counts = deaths.DEATHS.to_numpy(dtype=float)
    if not np.isfinite(counts).all() or (counts <= 0).any() or (counts % 1 != 0).any():
        raise ValueError('DEATHS must contain positive whole-number counts.')
    if deaths.duplicated(['LAT', 'LON']).any():
        raise ValueError('This location-based lesson expects one row per location.')
    if pumps.Street.isna().any():
        raise ValueError('Pump street names must be supplied by the source.')
    return deaths, pumps


def cluster_locations(deaths, radius_m=50, min_locations=5):
    """Fit unsupervised DBSCAN; radius is neighbor distance, not cluster diameter."""
    if isinstance(radius_m, bool) or not math.isfinite(radius_m) or not 1 <= radius_m <= 200:
        raise ValueError('Use a finite neighborhood radius from 1 to 200 meters.')
    if isinstance(min_locations, bool) or not isinstance(min_locations, int) or min_locations < 2:
        raise ValueError('Minimum core-neighborhood size must be an integer of at least two.')
    return DBSCAN(eps=radius_m / EARTH_RADIUS_M, min_samples=min_locations,
                  metric='haversine', algorithm='brute').fit_predict(coordinates(deaths))


def summary(deaths, labels):
    labels = np.asarray(labels)
    if labels.shape != (len(deaths),):
        raise ValueError('One cluster label is required for each location.')
    return (deaths.assign(group=labels).groupby('group', sort=True)
            .agg(locations=('FID', 'size'), recorded_deaths=('DEATHS', 'sum'))
            .reset_index())


def color_for(label):
    return UNASSIGNED if label == -1 else COLORS[int(label) % len(COLORS)]


def local_xy(frame):
    """Approximate local meter coordinates for display only; fitting uses haversine."""
    lon0, lat0 = -0.136, 51.513
    x = EARTH_RADIUS_M * math.cos(math.radians(lat0)) * np.radians(frame.LON.to_numpy() - lon0)
    y = EARTH_RADIUS_M * np.radians(frame.LAT.to_numpy() - lat0)
    return x, y


def plot_locations(deaths, labels=None, pumps=None, radius_m=50):
    """Offline analytical point map; no street tiles or hidden model fitting."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    x, y = local_xy(deaths)
    colors = '#374151' if labels is None else [color_for(int(label)) for label in labels]
    ax.scatter(x, y, c=colors, s=19, alpha=.9, linewidths=.25, edgecolors='white')
    if pumps is not None:
        px, py = local_xy(pumps)
        ax.scatter(px, py, marker='D', color='#b45309', s=70, edgecolors='white', label='Water pumps')
        for i, (xi, yi) in enumerate(zip(px, py), 1):
            ax.annotate(f'P{i}', (xi, yi), xytext=(7, 5), textcoords='offset points', fontsize=9)
        ax.legend(loc='lower left')
    ax.set(xlim=(-330, 350), ylim=(-355, 350), aspect='equal',
           xlabel='Local east–west distance (approximate meters)',
           ylabel='Local north–south distance (approximate meters)')
    title = '1. Map the recorded locations — no model yet'
    if labels is not None:
        groups = len(set(map(int, labels)) - {-1})
        title = f'{"3. Reveal pumps" if pumps is not None else "2. Find groups"} — {radius_m} m: {groups} group(s)'
    ax.set_title(title, fontsize=13)
    ax.grid(alpha=.16)
    fig.text(.5, .02, 'One dot = one recorded location. Colors are groups, not risk. Gray = unassigned.',
             ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .045, 1, 1))
    return fig


def geolibre_map(deaths, pumps, labels, radius_m=50, reveal_pumps=True):
    """Render already-computed labels with the existing JupyterLite-safe adapter."""
    from geolibre_lite import LiteMap
    labels = np.asarray(labels)
    summary(deaths, labels)  # length check; never fit a second, hidden model
    view = LiteMap(center=[-0.136, 51.513], zoom=15.8, height='580px')
    for label in sorted(set(map(int, labels))):
        features = []
        for row in deaths.loc[labels == label].itertuples():
            features.append({'type': 'Feature', 'id': int(row.FID),
                'geometry': {'type': 'Point', 'coordinates': [float(row.LON), float(row.LAT)]},
                'properties': {'source_FID': int(row.FID), 'recorded_deaths': int(row.DEATHS),
                               'group': label, 'neighbor_radius_m': radius_m,
                               'interpretation': 'Exploratory location group, not estimated disease risk'}})
        view.add_geojson({'type': 'FeatureCollection', 'features': features},
                        name='Unassigned locations' if label == -1 else f'Group {label}',
                        fillColor=color_for(label), circleRadius=5, fillOpacity=.85,
                        strokeColor='#ffffff', strokeWidth=.3)
    if reveal_pumps:
        features = [{'type': 'Feature', 'id': int(row.FID),
            'geometry': {'type': 'Point', 'coordinates': [float(row.LON), float(row.LAT)]},
            'properties': {'source_FID': int(row.FID), 'source_street': row.Street,
                           'label': f'P{i}', 'role': 'Context only; not supplied to DBSCAN'}}
            for i, row in enumerate(pumps.itertuples(), 1)]
        view.add_geojson({'type': 'FeatureCollection', 'features': features}, name='Water pumps — context only',
                        fillColor='#b45309', circleRadius=9, strokeColor='#ffffff', strokeWidth=2)
    return view
