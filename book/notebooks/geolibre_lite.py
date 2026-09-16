"""JupyterLite-safe GeoLibre adapter.

GeoLibre's normal ``Map`` widget serves its bundled web app from a localhost
HTTP server. That is appropriate for a normal CPython kernel, but Pyodide runs
inside the browser and cannot bind a TCP socket. ``LiteMap`` keeps GeoLibre's
project/layer builders while rendering the project with GeoLibre's hosted
viewer and official embed/postMessage protocol.

This module is intentionally small. It implements only the API used by the
notebooks in this repository.
"""

from __future__ import annotations

import json
from typing import Any

import anywidget
import traitlets

from geolibre import authoring as _authoring
from geolibre import project as _project


_HOSTED_VIEWER = "https://web.geolibre.app/"

_ESM = r"""
function render({ model, el }) {
  el.innerHTML = "";

  const frame = document.createElement("iframe");
  frame.style.width = "100%";
  frame.style.height = model.get("height") || "700px";
  frame.style.border = "0";
  frame.style.display = "block";
  frame.setAttribute("allow", "fullscreen");
  frame.setAttribute("allowfullscreen", "");

  const embeddedUrl = (url) => {
    const u = new URL(url);
    u.searchParams.set("embed", "1");
    return u.toString();
  };
  const origin = () => new URL(model.get("app_url")).origin;

  frame.src = embeddedUrl(model.get("app_url"));
  el.appendChild(frame);

  let ready = false;
  let seq = 0;
  const sendProject = () => {
    if (!ready || !frame.contentWindow) return;
    seq += 1;
    frame.contentWindow.postMessage(
      { type: "geolibre:load-project", project: model.get("project"), seq },
      origin(),
    );
  };

  const onMessage = (event) => {
    if (event.source !== frame.contentWindow) return;
    if (event.origin !== origin()) return;
    const data = event.data;
    if (data && data.type === "geolibre:ready") {
      ready = true;
      sendProject();
    }
  };

  const onProject = () => sendProject();
  const onHeight = () => {
    frame.style.height = model.get("height") || "700px";
  };
  const onAppUrl = () => {
    ready = false;
    frame.src = embeddedUrl(model.get("app_url"));
  };

  window.addEventListener("message", onMessage);
  model.on("change:project", onProject);
  model.on("change:height", onHeight);
  model.on("change:app_url", onAppUrl);

  return () => {
    window.removeEventListener("message", onMessage);
    model.off("change:project", onProject);
    model.off("change:height", onHeight);
    model.off("change:app_url", onAppUrl);
  };
}
export default { render };
"""


def _feature_collection(data: Any) -> dict[str, Any]:
    """Convert an inline GeoJSON-like object to a FeatureCollection dict."""
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LiteMap.add_geojson accepts an inline dict/JSON string. "
                "For a remote URL it creates a browser-fetched GeoLibre vector layer."
            ) from exc
        data = parsed

    if hasattr(data, "to_json"):
        data = json.loads(data.to_json())
    elif hasattr(data, "__geo_interface__"):
        data = data.__geo_interface__

    if not isinstance(data, dict):
        raise TypeError("GeoJSON input must be a dict, JSON string, or __geo_interface__ object")
    if data.get("type") == "FeatureCollection":
        return data
    if data.get("type") == "Feature":
        return {"type": "FeatureCollection", "features": [data]}
    raise ValueError("Expected a GeoJSON Feature or FeatureCollection")


def _normalise_rescale(rescale: Any) -> Any:
    """Accept leafmap-style [min,max] as well as GeoLibre's [[min,max], ...]."""
    if rescale is None:
        return None
    if (
        isinstance(rescale, (list, tuple))
        and len(rescale) == 2
        and all(isinstance(value, (int, float)) for value in rescale)
    ):
        return [[float(rescale[0]), float(rescale[1])]]
    return rescale


class LiteMap(anywidget.AnyWidget):
    """GeoLibre project widget that does not start a localhost server."""

    _esm = _ESM
    project = traitlets.Dict().tag(sync=True)
    app_url = traitlets.Unicode(_HOSTED_VIEWER).tag(sync=True)
    height = traitlets.Unicode("700px").tag(sync=True)

    def __init__(
        self,
        center: list[float] | tuple[float, float] | None = None,
        zoom: float | None = None,
        *,
        height: str = "700px",
        app_url: str = _HOSTED_VIEWER,
        renderer: str = "maplibre",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.height = height
        self.app_url = app_url
        self.project = _project.build_empty_project(
            center=center,
            zoom=zoom,
            renderer=renderer,
        )

    def _add_layer(self, layer: dict[str, Any]) -> str:
        project = dict(self.project)
        project["layers"] = list(project.get("layers", []))
        layer_id = _authoring.add_layer(project, layer)
        self.project = project
        return layer_id

    def add_geojson(self, data: Any, name: str = "GeoJSON", **style: Any) -> str:
        if isinstance(data, str) and data.startswith(("http://", "https://")):
            # The browser fetches the remote source. This avoids Python-side DNS
            # and socket calls that are not available in Pyodide.
            layer = _project.vector_layer(
                name,
                data,
                render_mode="geojson",
                data_format="geojson",
                **style,
            )
        else:
            layer = _project.geojson_layer(name, _feature_collection(data), **style)
        return self._add_layer(layer)

    def add_cog(
        self,
        url: str,
        name: str = "COG",
        *,
        bands: list[int] | None = None,
        colormap: str | None = None,
        rescale: Any = None,
        **style: Any,
    ) -> str:
        return self._add_layer(
            _project.cog_layer(
                name,
                url,
                bands=bands,
                colormap=colormap,
                rescale=_normalise_rescale(rescale),
                **style,
            )
        )

    def add_pmtiles(
        self,
        url: str,
        name: str = "PMTiles",
        *,
        tile_type: str = "vector",
        source_layers: list[str] | None = None,
        **style: Any,
    ) -> str:
        return self._add_layer(
            _project.pmtiles_layer(
                name,
                url,
                tile_type=tile_type,
                source_layers=source_layers,
                **style,
            )
        )

    def add_choropleth(
        self,
        data: Any,
        column: str,
        name: str = "Choropleth",
        *,
        class_count: int = 5,
        colormap: str = "viridis",
        scheme: str = "equal-interval",
        **style: Any,
    ) -> str:
        fc = _feature_collection(data)
        values = [
            feature.get("properties", {}).get(column)
            for feature in fc.get("features", [])
            if isinstance(feature, dict)
        ]
        classified = _authoring.build_choropleth_style(
            values,
            column,
            class_count=class_count,
            colormap=colormap,
            scheme=scheme,
        )
        classified.update(style)
        return self._add_layer(_project.geojson_layer(name, fc, **classified))

    def add_marker(
        self,
        lon: float,
        lat: float,
        name: str = "Marker",
        properties: dict[str, Any] | None = None,
        **style: Any,
    ) -> str:
        feature = {
            "type": "Feature",
            "properties": dict(properties or {}),
            "geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]},
        }
        return self.add_geojson(
            {"type": "FeatureCollection", "features": [feature]},
            name=name,
            **style,
        )

    def add_heatmap(
        self,
        points: Any,
        name: str = "Heatmap",
        *,
        radius: float = 30,
        intensity: float = 1,
        color_ramp: str = "turbo",
        weight_field: str = "",
        **style: Any,
    ) -> str:
        if hasattr(points, "to_dict"):
            points = points.to_dict("records")
        features = []
        for point in points:
            row = dict(point)
            lon = row.pop("lon", row.pop("lng", row.pop("longitude", None)))
            lat = row.pop("lat", row.pop("latitude", None))
            if lon is None or lat is None:
                raise ValueError("Heatmap records need lon/lng/longitude and lat/latitude")
            features.append(
                {
                    "type": "Feature",
                    "properties": row,
                    "geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]},
                }
            )
        style = {
            **style,
            "pointRenderer": "heatmap",
            "heatmapRadius": float(radius),
            "heatmapIntensity": float(intensity),
            "heatmapColorRamp": str(color_ramp),
            "heatmapWeightProperty": str(weight_field),
        }
        return self._add_layer(
            _project.geojson_layer(
                name,
                {"type": "FeatureCollection", "features": features},
                **style,
            )
        )

    def to_project(self) -> dict[str, Any]:
        """Return a credential-redacted, detached GeoLibre project dict."""
        return _project.redact_credentials(self.project)


Map = LiteMap
