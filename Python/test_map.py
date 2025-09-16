#!/usr/bin/env python3
"""
Simple test to verify basemap loading
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

# Simple test with just one point
sites = [{"name": "Korfu", "lat": 39.6243, "lon": 19.9217}]

df = pd.DataFrame(sites)
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])],
    crs="EPSG:4326"
)

# Project to web mercator
gdf_web = gdf.to_crs(epsg=3857)

# Create figure
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the point first
gdf_web.plot(ax=ax, color="red", markersize=200, zorder=10)

# Try to add basemap
try:
    # Use a larger buffer around the point
    point = gdf_web.geometry.iloc[0]
    buffer_size = 50000  # 50km buffer
    minx = point.x - buffer_size
    maxx = point.x + buffer_size  
    miny = point.y - buffer_size
    maxy = point.y + buffer_size
    
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    
    print("Adding basemap...")
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=8)
    print("Basemap added successfully!")
    
except Exception as e:
    print(f"Basemap failed: {e}")
    ax.set_facecolor('lightblue')

# Add title and save
ax.set_title("Test Map", fontsize=16)
plt.savefig("test_map.png", dpi=150, bbox_inches="tight")
plt.savefig("test_map.jpg", dpi=150, bbox_inches="tight")  # Also save as JPG
print("Test map saved as test_map.png and test_map.jpg")