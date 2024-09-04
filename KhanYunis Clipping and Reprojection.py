# -*- coding: utf-8 -*- *enhanced by chat gpt*
"""
Created on Sun Jul 28 11:18:39 2024

@author: ss1647
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:46:36 2024

@author: ss1647
"""

import subprocess
import sys

# put together
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# conda packages
install("geopandas")
install("rasterio")

# import all packages
import os
import glob
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import box

# define paths
shapefile_path = r'C:\Local Data\ss1647\Dissertation - Copy - Copy\Shapefiles\KhanYunis.geojson'
raster_files_dir = r'C:\Local Data\ss1647\Dissertation - Copy - Copy\Downloaded_bands_weekly'
output_dir = r'C:\Local Data\ss1647\Dissertation - Copy - Copy\Clipped_bands_weekly_KhanYunis'

# outputs
os.makedirs(output_dir, exist_ok=True)

# read
shapefile = gpd.read_file(shapefile_path)

# raster files
raster_files = glob.glob(os.path.join(raster_files_dir, '*.tif'))

# clip single raster out
def clip_raster(raster_path, shapes, output_path):
    with rasterio.open(raster_path) as src:
        # Ensure the shapefile and raster have the same CRS
        if shapefile.crs != src.crs:
            print(f"Reprojecting shapefile from {shapefile.crs} to {src.crs}")
            shapes = shapefile.to_crs(src.crs).geometry

        # Check if the shapefile geometry intersects with the raster extent
        raster_bounds = src.bounds
        raster_bbox = box(*raster_bounds)
        if not any(shape.intersects(raster_bbox) for shape in shapes):
            print(f"Skipping {raster_path} as it does not overlap with the shapefile.")
            return

        out_image, out_transform = mask(src, shapes, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(out_image)

# clip individual rasters
for raster_path in raster_files:
    raster_filename = os.path.basename(raster_path)
    output_path = os.path.join(output_dir, raster_filename)
    clip_raster(raster_path, shapefile.geometry, output_path)

print("clip complete")
