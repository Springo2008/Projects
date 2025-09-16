#!/usr/bin/env python3
"""
generate_ioniske_map.py
Genererer en høyoppløst PNG (2400x1600) med markører for:
Korfu, Lefkada, Meganisi (Vathy), Ithaka (Vathy),
Kefalonia (Sami, Argostoli), Zakynthos, Preveza, Nikopolis, Actium.

Kjør:
pip install geopandas contextily matplotlib pandas pyproj
python generate_ioniske_map.py
Output: ioniske_oykart.png
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

# Steder og anslåtte koordinater (lat, lon)
sites = [
    {"name": "Korfu (Korkyra)", "lat": 39.6243, "lon": 19.9217},
    {"name": "Lefkada (Leucas)", "lat": 38.8308, "lon": 20.7054},
    {"name": "Meganisi (Vathy)", "lat": 38.6600, "lon": 20.7500},
    {"name": "Ithaka (Vathy)", "lat": 38.3697, "lon": 20.7250},
    {"name": "Kefalonia (Sami)", "lat": 38.2460, "lon": 20.6230},
    {"name": "Kefalonia (Argostoli)", "lat": 38.1750, "lon": 20.4890},
    {"name": "Zakynthos (Zakynthos by)", "lat": 37.7870, "lon": 20.8990},
    {"name": "Preveza", "lat": 38.9560, "lon": 20.7500},
    {"name": "Nikopolis (ruinene)", "lat": 38.9381, "lon": 20.7148},
    {"name": "Actium (Aktio)", "lat": 38.9520, "lon": 20.6180},
]

# DataFrame -> GeoDataFrame
df = pd.DataFrame(sites)
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])],
    crs="EPSG:4326"
)

# Project to web mercator for tile overlay
gdf_web = gdf.to_crs(epsg=3857)

# Compute bounds and add margin
minx, miny, maxx, maxy = gdf_web.total_bounds
dx = (maxx - minx) * 0.15
dy = (maxy - miny) * 0.15
bbox = (minx - dx, miny - dy, maxx + dx, maxy + dy)

# Figure size chosen so that DPI * figsize = desired px
# We want 2400x1600 px -> figsize (12, 8) with dpi=200
fig, ax = plt.subplots(figsize=(12, 8), dpi=200)

# First, set the extent based on our data
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

# Plot basemap with multiple fallback options AFTER setting extent
basemap_loaded = False
tile_sources = [
    ctx.providers.OpenStreetMap.Mapnik,
    ctx.providers.CartoDB.Positron,
    ctx.providers.OpenStreetMap.DE,
    ctx.providers.CartoDB.Voyager
]

for source in tile_sources:
    try:
        print(f"Trying to load basemap from {source['name']}...")
        # Use alpha to make basemap slightly transparent and zorder to put it behind points
        ctx.add_basemap(ax, source=source, zoom=10, alpha=0.8, zorder=1)
        print(f"Successfully loaded basemap from {source['name']}")
        basemap_loaded = True
        break
    except Exception as e:
        print(f"Failed to load {source['name']}: {e}")
        continue

if not basemap_loaded:
    print("Warning: Could not load any basemap tiles. Adding simple background.")
    # Add a simple background color to show the area
    ax.set_facecolor('#e6f3ff')

# Plot points on top of the basemap
gdf_web.plot(ax=ax, color="#d73027", edgecolor="black", markersize=120, zorder=5)

# Add labels with offsets (adjust offsets per point if overlapping)
for idx, row in gdf_web.iterrows():
    x, y = row.geometry.x, row.geometry.y
    name = row["name"]
    ax.annotate(name, xy=(x, y), xytext=(4, -14), textcoords="offset points",
                fontsize=14, fontweight="bold", color="#073642", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, linewidth=0.5))

# Remove axis decorations
ax.set_axis_off()

# Save PNG
output_filename = "ioniske_oykart.png"
plt.savefig(output_filename, bbox_inches="tight", pad_inches=0.05)
print(f"Saved map to {output_filename}")